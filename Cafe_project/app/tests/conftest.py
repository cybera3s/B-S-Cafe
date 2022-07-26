import os
import pytest
from flask import template_rendered

from app import create_app
from app.database import db
from app.database import db as _db

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

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    # ctx = flask_app.app_context()
    rctx = flask_app.test_request_context()
    # ctx.push()
    rctx.push()

    yield testing_client  # this is where the testing happens!

    # ctx.pop()
    rctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()