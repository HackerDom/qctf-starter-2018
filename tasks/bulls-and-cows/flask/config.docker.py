import os

def getenv(variable_name):
    value = os.getenv(variable_name, None)
    if value is None:
        raise ValueError('Please specify the "{}" environment variable'
                         .format(variable_name))
    return value

SECRET_KEY = getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = getenv('POSTGRES_CONNECTION_STRING')
FLAG = getenv('FLAG')
SCHEME = getenv('SCHEME')
