import os


def getenv(variable_name):
    value = os.getenv(variable_name, None)
    if value is None:
        raise ValueError('Please specify the "{}" environment variable'
                         .format(variable_name))
    return value


DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_TOKEN = getenv('MAIL_TOKEN')
MAIL_DEFAULT_SENDER = 'notemaster.noreply@contest.qctf.ru'
