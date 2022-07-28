from flask import url_for
from unittest import TestCase
from app import create_app
from app.extensions import db
from app.models import *


class BaseTest(TestCase):
    def setUp(self):
        app = create_app('config.TestConfig')
        self.client = app.test_client()
        db.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()


class TestRoutes(BaseTest):

    def test_get_request_index_should_have_succeed(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Home</title>", response.data)

    def test_post_request_index_should_fail(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 405)

    def test_get_request_home_should_succeed(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_get_request_menu_should_succeed(self):
        response = self.client.get('/menu')
        self.assertEqual(response.status_code, 200)

    def test_get_request_order_non_existing_table_should_fail(self):
        response = self.client.get('/order/1')
        self.assertEqual(response.status_code, 404)

    def test_get_request_order_existing_table_should_succeed(self):
        new_table = Table(capacity=4, position='any')
        new_table.create()
        response = self.client.get('/order/' + str(new_table.id))
        self.assertEqual(response.status_code, 200)

    def test_get_request_order_should_set_cookies(self):
        new_table = Table(capacity=4, position='any')
        new_table.create()
        response = self.client.get('/order/' + str(new_table.id))

        cookies_list = list(filter(lambda i: i[0] == 'Set-Cookie', response.headers))

        self.assertIn(('Set-Cookie', f'table_id={new_table.id}; Path=/'), cookies_list)
        self.assertIn(('Set-Cookie', 'receipt=pending; Path=/'), cookies_list)
        self.assertEqual(response.status_code, 200)

    def test_get_request_order_busy_table_should_fail(self):
        new_table = Table(capacity=4, position='any', status=True)
        new_table.create()
        response = self.client.get('/order/' + str(new_table.id))

        self.assertEqual(response.data, b'Table is Busy')
        self.assertEqual(response.status_code, 400)

