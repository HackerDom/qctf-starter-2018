import os

from flask import Flask, render_template, request, url_for, redirect, g, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from email_confirmations.models import db, User, Note
from email_confirmations.forms import LoginForm, RegistrationForm, NewNoteForm
from email_confirmations.utils import mail_manager, send_confirmation_email


app = Flask(__name__)
app.config.from_object('default_config')
if os.getenv('ENVIRONMENT') == 'DEV':
    app.config.from_object('development_config')
else:
    app.config.from_envvar('APP_CONFIG')
app.jinja_env.add_extension('jinja2.ext.do')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def add_user():
    g.user = current_user


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    errors = False

    form = NewNoteForm(request.form)
    if request.method == 'POST':
        if form.validate():
            db.session.add(form.note)
            db.session.commit()
        else:
            errors = True

    user_notes = Note.query \
        .filter_by(author=current_user) \
        .order_by(Note.id) \
        .all()
    if request.method == 'POST' and not errors:
        return redirect(url_for('index'))
    else:
        return render_template('index.html', notes=user_notes, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = False
    registration_form = RegistrationForm()
    login_form = LoginForm()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'register':
            registration_form.process(request.form)
            if registration_form.validate():
                db.session.add(registration_form.user)
                db.session.commit()

                errors = True
                try:
                    send_confirmation_email(registration_form.user)
                    registration_form.password.errors.append(
                        'To complete the registration, please check your email')
                except Exception:
                    db.session.delete(registration_form.user)
                    db.session.commit()
                    registration_form.password.errors.append(
                        'Registration failed. Please try again')
            else:
                errors = True

        elif action == 'login':
            login_form.process(request.form)
            if login_form.validate():
                login_user(login_form.user, remember=True)
                return redirect(request.args.get('next') or url_for('index'))
            else:
                errors = True

    if request.method == 'POST' and not errors:
        return redirect(url_for('login'))
    else:
        return render_template('login.html', login_form=login_form, registration_form=registration_form)


@app.route('/confirm/<user_id>')
def confirm(user_id):
    user = load_user(user_id)
    if user is None:
        return abort(404)

    user.confirmed = True
    db.session.commit()
    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
