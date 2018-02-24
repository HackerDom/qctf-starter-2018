from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, RadioField
from wtforms.validators import Required, Length

class EncryptForm(FlaskForm):
    data_format = RadioField('data_format', choices=[('plain','Plain'), ('base64', 'Base64')], validators = [Required()])
    data = TextAreaField('data', validators = [Required(), Length(max=1000)])
