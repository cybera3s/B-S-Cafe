from flask import url_for
from unittest import TestCase
from app import create_app
from app.database import db


class TestURLs(TestCase):
    def setUp(self):
        app = create_app('config.TestConfig')
        self.client = app.test_client()
        db.app = app
        db.create_all()

    def test_get_request_index_should_have_succeed(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Home</title>", response.data)

    def test_post_request_index_should_fail(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 405)

    def tearDown(self):
        db.session.remove()

# def test_get_request_index_should_succeed(client):
#     url = url_for('landing.index')
#     response = client.get(url)
#     assert b"<title>Home</title>" in response.data
#     assert response.status_code == 200
#
#
# def test_post_request_index_should_fail(client):
#     url = url_for('landing.index')
#     response = client.post(url)
#     assert response.status_code == 405
#
#
# def test_get_request_index_should_have_table_context(client, captured_templates):
#     url = url_for('landing.index')
#     response = client.get(url)
#
#     template, context = captured_templates[0]
#
#     assert 'tables' in context
#     assert template.name == "landing/index.html"
