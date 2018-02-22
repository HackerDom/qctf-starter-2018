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
    files = list_files_with_fakes(current_user)
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

    error = None
    try:
        if os.path.splitext(file_part.filename)[1] == '.tar':
            error = process_tar_or_get_error(file_part, current_user)
        else:
            error = process_usual_file_or_get_error(file_part, current_user)
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
    error = get_path_validation_error_or_none(path, current_user)
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
    error = get_path_validation_error_or_none(path, current_user)
    if error is not None:
        return error
    try:
        os.remove(path)
    except Exception:
        return build_error('Invalid path')
    return redirect('/')

def process_tar_or_get_error(file_part, current_user):
    files_count = len(list_files_for_user(current_user.directory, current_user.login, True))
    tmp_user_dir = get_tmp_user_dir(current_user)
    tar_path = os.path.join(tmp_user_dir, file_part.filename)
    if not is_valid_tmp_path(tar_path, current_user):
        return 'Invalid filename'
    if os.path.exists(tar_path):
        return 'Invalid filename'
    file_part.save(tar_path)
    with tarfile.open(tar_path, 'r:') as tar:
        if len(tar.getnames) + files_count > app.config['MAX_FILES_COUNT_PER_USER']:
            return 'There will be too many files in your directory after upload: not more than {} is allowed'.format(app.config['MAX_FILES_COUNT_PER_USER'])
        for tarinfo in tar:
            if not (tarinfo.isreg() or tarinfo.issym()):
                continue
            if tarinfo.issym():
                if not is_valid_link_path(tarinfo.linkname, current_user):
                    continue
            result_path = os.path.join(tmp_user_dir, tarinfo.name)
            if is_valid_tmp_path(result_path, current_user):
                tar.extract(tarinfo, path=tmp_user_dir)
                os.rename(result_path, os.path.join(get_user_dir(current_user), os.path.split(result_path)[-1]))
    os.remove(tar_path)

def process_usual_file_or_get_error(file_part, current_user):
    files_count = len(list_files_for_user(current_user.directory, current_user.login, True))
    if files_count + 1 > app.config['MAX_FILES_COUNT_PER_USER']:
        return 'There will be too many files in your directory after upload: not more than {} is allowed'.format(app.config['MAX_FILES_COUNT_PER_USER'])
    path = os.path.join(get_user_dir(current_user), file_part.filename)
    if not is_valid_path(path, current_user):
        return 'Invalid filename'
    if os.path.exists(path):
        return 'File already exists'
    file_part.save(path)

def get_path_validation_error_or_none(path, current_user):
    if path is None:
        return build_error('Path is requied')
    if not is_valid_path(path, current_user):
        if is_valid_fake_user_path(path, current_user):
            return build_error('Permission denied: you do not own this file')
        return build_error('Invalid path')
    if not os.path.isfile(path):
        return build_error('No such file')

def is_valid_path(path, current_user):
    current_user_dir = get_user_dir_internal(current_user.directory, current_user.login)
    path = os.path.abspath(path)
    return path.startswith(current_user_dir)

def is_valid_tmp_path(path, current_user):
    current_user_dir = get_tmp_user_dir(current_user)
    path = os.path.abspath(path)
    return path.startswith(current_user_dir)

def is_valid_fake_user_path(path, current_user):
    path = os.path.abspath(path)
    for fake_user in app.config["FAKE_USERS"]:
        fake_user_dir = get_user_dir_internal(current_user.directory, fake_user)
        if path.startswith(fake_user_dir):
            return True
    return False

def is_valid_link_path(path, current_user):
    if os.path.isabs(path):
        return is_valid_path(path, current_user) or is_valid_fake_user_path(path, current_user)
    abs_path = os.path.join(get_user_dir(current_user), path)
    return is_valid_path(abs_path, current_user) or is_valid_fake_user_path(abs_path, current_user)

def list_files_for_user(current_user_dir, user_name, personal):
    user_dir = get_user_dir_internal(current_user_dir, user_name)
    entries = [{'name': x, 'path': os.path.join(user_dir, x), 'personal': personal, 'owner': user_name} for x in os.listdir(user_dir)]
    return [entry for entry in entries if os.path.isfile(entry['path']) or os.path.islink(entry['path'])]

def list_files_with_fakes(current_user):
    result = list_files_for_user(current_user.directory, current_user.login, True)
    for fake_user in app.config["FAKE_USERS"]:
        result += list_files_for_user(current_user.directory, fake_user, False)
    return result

def get_user_dir(current_user):
    return get_user_dir_internal(current_user.directory, current_user.login)

def get_user_dir_internal(directory, login):
    if not is_safe_path_path(directory) or not is_safe_path_path(login):
        raise Exception('Unsafe dir or username: "{}" "{}"'.format(directory, login))
    current_user_dir = os.path.join(app.config['USER_DATA_DIR'], directory, login)
    ensure_dir_exists(current_user_dir)
    return os.path.abspath(current_user_dir)

def get_tmp_user_dir(current_user):
    if not is_safe_path_path(current_user.directory) or not is_safe_path_path(current_user.login):
        raise Exception('Unsafe dir or username: "{}" "{}"'.format(current_user.directory, current_user.login))
    current_user_dir = os.path.join(app.config['TMP_USER_DATA_DIR'], current_user.directory, current_user.login)
    ensure_dir_exists(current_user_dir)
    return os.path.abspath(current_user_dir)

def is_safe_path_path(user_name):
    return re.fullmatch('[a-zA-Z0-9]+', user_name) != None

def ensure_dir_exists(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if not os.path.isdir(dir_name):
        raise Exception('User path "{}" exists, but it is not a directory'.format(dir_name))
