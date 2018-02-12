from sqlalchemy import or_, exists
from wtforms import Form, StringField, PasswordField, validators

from email_confirmations.models import db, User


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.InputRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        if not super().validate():
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False
        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.InputRequired()])
    email = StringField('Email address', [validators.Length(min=6, max=100)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        if not super().validate():
            return False

        if User.query.filter_by(username=self.username.data).first():
            self.username.errors.append('Username already taken')
            return False
        if User.query.filter_by(email=self.email.data).first():
            self.email.errors.append('Email already in use')
            return False

        self.user = User.with_password(
            username=self.username.data,
            password=self.password.data,
            email=self.email.data)
        return True
