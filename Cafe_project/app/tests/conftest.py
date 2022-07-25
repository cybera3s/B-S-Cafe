import os
import pytest
from app import create_app
from app.database import db as _db


BASE_DIR= os.path.abspath(os.path.dirname(__file__))


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(BASE_DIR, 'test_cafe.db')
    })

    yield app



@pytest.fixture()
def db(app):
    """Returns session-wide initialized data"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()