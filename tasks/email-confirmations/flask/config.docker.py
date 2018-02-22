from email_confirmations.default_config import getenv

SECRET_KEY = getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = getenv('POSTGRES_CONNECTION_STRING')
