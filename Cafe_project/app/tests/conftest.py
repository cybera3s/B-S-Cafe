import os
import pytest
from flask import template_rendered

from app import create_app
from app.extensions import db
from app.extensions import db as _db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='function')
def app():
    app = create_app('config.TestConfig')

    db.app = app
    db.create_all()
    yield app
    db.session.remove()
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    app.test_request_context().push()
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('config.TestConfig')
    db.app = flask_app
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    app_context = flask_app.app_context()
    request_context = flask_app.test_request_context()
    app_context.push()
    request_context.push()

    yield testing_client  # this is where the testing happens!
    app_context.pop()
    request_context.pop()
    db.session.remove()


@pytest.fixture(scope='function')
def init_database():
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!
    db.drop_all()
