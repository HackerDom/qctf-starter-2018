from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from flask_login import current_user

from email_confirmations.models import User, Note


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
        if not user.confirmed:
            self.username.errors.append('User\'s email not confirmed. Please check your email')
            return False

        self.user = user
        return True


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.InputRequired()])
    email = StringField('Email address', [validators.Length(min=6, max=100), validators.email()])

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


class NewNoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    content = TextAreaField('Content', [validators.Length(min=0, max=5000)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.note = None

    def validate(self):
        if not super().validate():
            return False

        self.note = Note(
            title=self.title.data,
            content=self.content.data,
            author=current_user)
        return True
