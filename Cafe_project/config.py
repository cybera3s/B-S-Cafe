import os
from os import urandom

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    pass


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
    CSRF_SESSION_KEY = urandom(24)

    # Secret key for signing cookies
    SECRET_KEY = urandom(24)


class TestConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False