import os
import tarfile
import re
import urllib.parse

from flask import render_template, flash, redirect, request, send_file, make_response
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user

from app import app, login_manager
from app.nocache import nocache
from app.forms import LoginForm
from app.users import User, UserProvider

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
@login_required
def index():
    user_id = current_user.login
    files = list_files_with_fakes(user_id)
    return render_template('index.html', files=files)

@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = UserProvider.find_user(login_form.login.data)
        if user is None or user.password != login_form.password.data:
            return build_error('Wrong login or password')
        login_user(user)
        return redirect('/')
    return render_template('login.html', form=login_form)

@app.route('/register', methods=["GET", "POST"])
def register():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = UserProvider.create_user(login_form.login.data, login_form.password.data)
        if user is None:
            return build_error('User already exists')
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=login_form)

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')

def build_error(text):
    back_url = request.referrer
    if back_url is None:
        return render_template('error.html', error=text)
    return render_template('error.html', error=text, back_url=back_url)

@app.route('/upload', methods=["POST"])
@login_required
def upload():
    if 'file' not in request.files:
        return 'No file part', 400
    file_part = request.files['file']
    if file_part is None or file_part.filename == '':
        return build_error('No selected file')

    user_id = current_user.login
    error = None
    try:
        if os.path.splitext(file_part.filename)[1] == '.tar':
            error = process_tar_or_get_error(file_part, user_id)
        else:
            error = process_usual_file_or_get_error(file_part, user_id)
    except Exception:
        error = 'Invalid file or filename'
    if error is not None:
        return build_error(error)
    return redirect('/')

@app.route('/download')
@login_required
@nocache
def download():
    path = request.args.get('path')
    used_id = current_user.login
    error = get_path_validation_error_or_none(path, used_id)
    if error is not None:
        return error
    try:
        response = make_response(send_file(path, as_attachment=True))
        response.headers["Content-Disposition"] = \
            "attachment; " \
            "filenane={ascii_filename};" \
            "filename*=UTF-8''{utf_filename}".format(
            ascii_filename="file",
            utf_filename=urllib.parse.quote(os.path.basename(path))
        )
        return response
    except Exception:
        return build_error('Invalid path')

@app.route('/delete')
@login_required
@nocache
def delete():
    path = request.args.get('path')
    used_id = current_user.login
    error = get_path_validation_error_or_none(path, used_id)
    if error is not None:
        return error
    try:
        os.remove(path)
    except Exception:
        return build_error('Invalid path')
    return redirect('/')

def process_tar_or_get_error(file_part, user_id):
    tmp_user_dir = get_tmp_user_dir(user_id)
    tar_path = os.path.join(tmp_user_dir, file_part.filename)
    if not is_valid_tmp_path(tar_path, user_id):
        return 'Invalid filename'
    if os.path.exists(tar_path):
        return 'Invalid filename'
    file_part.save(tar_path)
    with tarfile.open(tar_path, 'r:') as tar:
        for tarinfo in tar:
            if not (tarinfo.isreg() or tarinfo.issym()):
                continue
            if tarinfo.issym():
                if not is_valid_link_path(tarinfo.linkname, user_id):
                    continue
            result_path = os.path.join(tmp_user_dir, tarinfo.name)
            if is_valid_tmp_path(result_path, user_id):
                tar.extract(tarinfo, path=tmp_user_dir)
                os.rename(result_path, os.path.join(get_user_dir(user_id), os.path.split(result_path)[-1]))
    os.remove(tar_path)

def process_usual_file_or_get_error(file_part, user_id):
    path = os.path.join(get_user_dir(user_id), file_part.filename)
    if not is_valid_path(path, user_id):
        return 'Invalid filename'
    if os.path.exists(path):
        return 'File already exists'
    file_part.save(path)

def get_path_validation_error_or_none(path, used_id):
    if path is None:
        return build_error('Path is requied')
    if not is_valid_path(path, used_id):
        if is_valid_fake_user_path(path):
            return build_error('Permission denied: you do not own this file')
        return build_error('Invalid path')
    if not os.path.isfile(path):
        return build_error('No such file')

def is_valid_path(path, user_id):
    current_user_dir = get_user_dir(user_id)
    path = os.path.normpath(path)
    return path.startswith(current_user_dir)

def is_valid_tmp_path(path, user_id):
    current_user_dir = get_tmp_user_dir(user_id)
    path = os.path.normpath(path)
    return path.startswith(current_user_dir)

def is_valid_fake_user_path(path):
    for fake_user in app.config["FAKE_USERS"]:
        if is_valid_path(path, fake_user):
            return True
    return False

def is_valid_link_path(path, user_id):
    if os.path.isabs(path):
        return is_valid_path(path, user_id) or is_valid_fake_user_path(path)
    abs_path = os.path.join(get_user_dir(user_id), path)
    return is_valid_path(abs_path, user_id) or is_valid_fake_user_path(abs_path)

def list_files_for_user(user_name, personal):
    current_user_dir = get_user_dir(user_name)
    entries = [{'name': x, 'path': os.path.join(current_user_dir, x), 'personal': personal, 'owner': user_name} for x in os.listdir(current_user_dir)]
    return [entry for entry in entries if os.path.isfile(entry['path']) or os.path.islink(entry['path'])]

def list_files_with_fakes(user_name):
    result = list_files_for_user(user_name, True)
    for fake_user in app.config["FAKE_USERS"]:
        result += list_files_for_user(fake_user, False)
    return result

def get_user_dir(user_name):
    if not is_safe_username(user_name):
        raise Exception('Unsafe username: "{}"'.format(user_name))
    current_user_dir = os.path.join(app.config['USER_DATA_DIR'], user_name)
    ensure_dir_exists(current_user_dir)
    if not os.path.isabs(current_user_dir):
        raise Exception('Not an absolute path: "{}"'.format(current_user_dir))
    return os.path.normpath(current_user_dir)

def get_tmp_user_dir(user_name):
    if not is_safe_username(user_name):
        raise Exception('Unsafe username: "{}"'.format(user_name))
    current_user_dir = os.path.join(app.config['TMP_USER_DATA_DIR'], user_name)
    ensure_dir_exists(current_user_dir)
    if not os.path.isabs(current_user_dir):
        raise Exception('Not an absolute path: "{}"'.format(current_user_dir))
    return os.path.normpath(current_user_dir)

def is_safe_username(user_name):
    return re.fullmatch('[a-zA-Z0-9]+', user_name) != None

def ensure_dir_exists(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    if not os.path.isdir(dir_name):
        raise Exception('User path "{}" exists, but it is not a directory'.format(dir_name))
