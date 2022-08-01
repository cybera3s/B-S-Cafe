import os
from os import urandom
from dotenv import load_dotenv

load_dotenv('.env')

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SITE_NAME = 'Cafe Bitter & Sweet'
    CSRF_SESSION_KEY = urandom(24)

    # Secret key for signing cookies
    SECRET_KEY = urandom(24)


class ProdConfig(Config):
    pass


class DevConfig(Config):
    # Statement for enabling the development environment
    DEBUG = True
    # Define the data - we are working with -> SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'cafe.db')
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # upload config
    UPLOAD_FOLDER = "app/static/images/menu_items"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 5 * 1000 * 1000  # set maximum volume to 5 MB for a uploaded content
    THREADS_PER_PAGE = 2
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    CSRF_SESSION_KEY = '12345678987654321'

    # Secret key for signing cookies
    SECRET_KEY = '12345678987654321'
    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PORT = os.getenv('MAIL_PORT', 465)
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_IMPORTS = ("app.landing.tasks",)


class TestConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
