import os


def getenv(variable_name):
    value = os.getenv(variable_name, None)
    if value is None:
        raise ValueError('Please specify the "{}" environment variable'
                         .format(variable_name))
    return value


DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = getenv('MAIL_USERNAME')
MAIL_PASSWORD = getenv('MAIL_PASSWORD')
EMAIL_FROM = MAIL_USERNAME
