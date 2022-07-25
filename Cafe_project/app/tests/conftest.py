import os
import pytest
from flask import template_rendered

from app import create_app
from app.database import db
from app.database import db as _db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture()
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

#
# @pytest.fixture()
# def db(app):
#     """Returns session-wide initialized data"""
#     with app.app_context():
#         _db.create_all()
#         yield _db
#         _db.drop_all()
