from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Regexp

class LoginForm(FlaskForm):
    login = TextField('login', validators = [Required(), Regexp('^[a-zA-Z0-9]+$')])
    password = PasswordField('password', validators = [Required()])
