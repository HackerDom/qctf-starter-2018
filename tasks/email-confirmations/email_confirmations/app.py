import os

from flask import Flask, render_template, request, url_for, redirect, g, abort
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message

from email_confirmations.models import db, User
from email_confirmations.forms import LoginForm, RegistrationForm


app = Flask(__name__)
app.config.from_object('default_config')
if os.getenv('ENVIRONMENT') == 'DEV':
    app.config.from_object('development_config')
else:
    app.config.from_envvar('APP_CONFIG')

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
mail = Mail(app)


def send_email(to, subject, content):
    msg = Message(
        subject,
        recipients=[to],
        html=content,
        sender=app.config['EMAIL_FROM'])
    mail.send(msg)


def send_confirmation_email(user):
    send_email(
        to=user.email,
        subject='Confirm your email',
        content=render_template(
            'activation_email.html',
            user=user,
            confirmation_url=url_for('confirm', user_id=user.id, _external=True)))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def add_user():
    g.user = current_user


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_user(form.user, remember=True)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        db.session.add(form.user)
        db.session.commit()
        send_confirmation_email(form.user)
        return render_template('register.html', form=form, show_confirmation_message=True)
    return render_template('register.html', form=form)


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
