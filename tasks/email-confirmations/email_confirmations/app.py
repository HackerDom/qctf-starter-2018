import os

from flask import Flask, render_template, request, url_for, redirect, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash

from email_confirmations.models import db, User


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
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password_hash, password):
        return render_template(
            'login.html', error='Incorrect username or password')

    login_user(user)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    if User.query.filter_by(username=username).first():
        return render_template('register.html', error='Username already in use')

    if User.query.filter_by(email=email).first():
        return render_template('register.html', error='Email already in use')

    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash, email=email)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
