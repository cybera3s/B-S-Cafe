from .conftest import test_client as client, init_database as init_db, captured_templates
from app.models import *
from flask import url_for
import json
import pytest


@pytest.mark.skip
def test_get_request_index_should_have_table_context(client, captured_templates):
    url = url_for('landing.index')
    response = client.get(url)

    template, context = captured_templates[0]

    assert 'tables' in context
    assert template.name == "landing/index.html"


def test_get_request_index_should_have_succeed(client, init_db):
    """
        GIVEN a Flask application, and database session
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data


def test_post_request_index_should_fail(client, init_db):
    """
        GIVEN a Flask application and database session
        WHEN the '/' page is requested (POST)
        THEN check the response is valid and method not allowed
    """
    response = client.post(url_for('landing.index'))
    assert response.status_code == 405


def test_get_request_home_should_succeed(client, init_db):
    """
        GIVEN a Flask application and database session
        WHEN the '/home' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get(url_for('landing.home'))
    assert response.status_code == 200


def test_get_request_menu_should_succeed(client, init_db):
    """
        GIVEN a Flask application and database session
        WHEN the '/menu' page is requested (GET)
        THEN check the response is valid
    """
    response = client.get(url_for('landing.menu'))
    assert response.status_code == 200


def test_get_request_order_non_existing_table_should_fail(client, init_db):
    """
        GIVEN a Flask application and database session
        WHEN the '/order/132' page is requested (GET)
        THEN check the response is valid and corresponding table not found
    """
    response = client.get(url_for('landing.order', table_id=132))
    assert response.status_code == 404


def test_get_request_order_existing_table_should_succeed(client, init_db):
    """
        GIVEN a Flask application and database session
        WHEN the '/order/new_table_id' page is requested (GET)
        THEN check the response is valid and corresponding table is selected
    """
    new_table = Table(capacity=4, position='any')
    new_table.create()
    response = client.get(url_for('landing.order', table_id=new_table.id))
    assert response.status_code == 200


def test_get_request_order_should_set_cookies(client, init_db):
    """
       GIVEN a Flask application and database session
       WHEN the '/order/new_table_id' page is requested (GET)
       THEN check the response has table_id cookies and is valid
   """
    new_table = Table(capacity=4, position='any')
    new_table.create()
    response = client.get(url_for('landing.order', table_id=new_table.id))

    cookies_list = list(filter(lambda i: i[0] == 'Set-Cookie', response.headers))
    print(cookies_list)
    assert ('Set-Cookie', f'table_id={new_table.id}; Path=/') in cookies_list
    assert response.status_code == 200


def test_get_request_order_busy_table_should_fail(client, init_db):
    """
       GIVEN a Flask application and database session
       WHEN the '/order/new_table_id' page is requested (GET) with busy table
       THEN check the response is valid
   """
    new_table = Table(capacity=4, position='any', status=True)
    new_table.create()
    response = client.get(url_for('landing.order', table_id=new_table.id))

    assert response.data == b'Table is Busy'
    assert response.status_code == 400


def test_post_request_order_without_body_should_fail(client, init_db):
    """
       GIVEN a Flask application and database session
       WHEN the '/order/new_table_id' page without body is requested (POST)
       THEN check the response is valid
   """
    new_table = Table(capacity=4, position='any', status=True)
    new_table.create()
    response = client.post(url_for('landing.order', table_id=new_table.id))
    assert response.status_code == 400
    assert b"Request Body is not provided" in response.data


def test_post_request_order_with_bad_body_should_fail(client, init_db):
    """
       GIVEN a Flask application and database session
       WHEN the '/order/new_table_id' page with bad body is requested (POST)
       THEN check the response is BAD REQUEST -> 400 status code
    """

    new_table = Table(capacity=4, position='any', status=True)
    new_table.create()
    body = {
        'itemId': 1,
        'itemName': 'tea',
        'finalPrice': 10
    }
    response = client.post(url_for('landing.order', table_id=new_table.id), json=body)
    assert response.status_code == 400
    assert response.data == b'one of the (menu item id,count,name,price,final price) is not provided!'


@pytest.mark.skip
def test_post_request_order_with_right_body_no_receipt_pending_should_fail(client, init_db):
    """
       GIVEN a Flask application and database session
       WHEN the '/order/new_table_id' page is requested (POST) with body and no receipt pending in cookies
       THEN check the response is BAD REQUEST -> 400 status code
    """
    new_table = Table(capacity=4, position='any', status=True)
    new_table.create()
    body = {
        'itemId': 1,
        'itemCount': 3,
        'itemName': 'tea',
        'itemPrice': 10,
        'finalPrice': 10
    }
    response = client.post(url_for('landing.order', table_id=new_table.id), json=body)
    assert response.status_code == 400
    assert response.data == b"You have no Receipt yet!"


def test_post_request_order_with_right_body_should_succeed(client, init_db):
    """
       GIVEN a Flask application and database session
       WHEN the '/order/new_table_id' page is requested (POST) with body and receipt pending in cookies
       THEN check the response is valid -> 200 and orders set in cookies
    """
    new_table = Table(capacity=4, position='any', status=True)
    new_table.create()
    body = {
        'itemId': 1,
        'itemCount': 3,
        'itemName': 'tea',
        'itemPrice': 10,
        'finalPrice': 10
    }
    client.set_cookie('localhost', 'receipt', 'pending')
    response = client.post(url_for('landing.order', table_id=new_table.id), json=body)

    assert response.status_code == 200
    res = client.get('/')   # to catch cookies from request
    assert 'orders' in res.request.cookies
    cookies_orders = json.loads(res.request.cookies.get('orders'))
    assert cookies_orders['1']['name'] == 'tea'