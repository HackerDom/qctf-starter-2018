import os

from flask import Flask, render_template, request, url_for, redirect, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

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


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


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
        login_user(form.user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
