from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    TESTING = environ.get('TESTING')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI',
                                          'mysql+pymysql://root:rootpassword@localhost:3306/instant_messaging')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
