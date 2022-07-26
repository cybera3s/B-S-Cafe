from .conftest import test_client as client, init_database as init_db, captured_templates
from app.models import *
from flask import url_for
import json
import pytest


@pytest.mark.skip
def test_get_request_index_should_have_table_context(client, captured_templates):
    url = url_for('landing.index')
    client.get(url)

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
    res = client.get('/')  # to catch cookies from request
    assert 'orders' in res.request.cookies
    cookies_orders = json.loads(res.request.cookies.get('orders'))
    assert cookies_orders['1']['name'] == 'tea'


def test_post_order_with_empty_order_in_cookies_should_pass(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/order/new_table_id' page is requested (POST) with empty orders in cookies
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
    client.set_cookie('orders', json.dumps([]))  # set empty orders in cookies
    response = client.post(url_for('landing.order', table_id=new_table.id), json=body)
    assert response.status_code == 200


# Cart View Tests

def test_add_to_cart_repetitive_item_should_increase_count(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/order/new_table_id' page is requested (POST) with orders and repetitive item in cookies
      THEN check the response is valid -> 200 and  repetitive item has increased it's count
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
    # set cookies
    client.set_cookie('localhost', 'receipt', 'pending')
    orders = {
        str(body['itemId']): {
            'count': 1,
            "name": body['itemName'],
            "price": body['itemPrice'],
            "item_final_price": body['finalPrice']
        }
    }
    client.set_cookie('localhost', 'orders', json.dumps(orders))

    response = client.post(url_for('landing.order', table_id=new_table.id), json=body)

    assert response.status_code == 200
    res = client.get('/')  # to catch cookies from request
    assert 'orders' in res.request.cookies
    cookies_orders = json.loads(res.request.cookies.get('orders'))
    assert cookies_orders['1']['name'] == 'tea'
    # increased count
    assert cookies_orders['1']['count'] == 4


@pytest.mark.skip
def test_get_cart_with_no_cookies_should_fail(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (GET) with empty orders in cookies
      THEN check the response is valid -> 400
    """
    response = client.get(url_for('landing.cart'))
    assert response.status_code == 400
    assert b"There is no orders" in response.data


def test_get_cart_with_bad_cookies_should_fail(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (GET) with empty orders in cookies
      THEN check the response is valid -> 400
    """
    client.set_cookie('localhost', 'orders', json.dumps({}))
    response = client.get(url_for('landing.cart'))

    assert response.status_code == 400
    assert b'Empty or Bad Orders Type' in response.data


def test_get_cart_with_right_cookies_should_succeed(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (GET) with correct orders in cookies
      THEN check the response is valid -> 200
    """
    orders = {
        '1': {
            'count': 1,
            "name": 'Tea',
            "price": 10,
            "item_final_price": 10
        }
    }
    client.set_cookie('localhost', 'orders', json.dumps(orders))
    response = client.get(url_for('landing.cart'))

    assert response.status_code == 200
    assert b"Final Price" in response.data
    assert b"Total Price" in response.data
    assert response.mimetype == 'text/html'


def test_post_cart_with_no_body_should_fail(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (POST) with no body
      THEN check the response is valid -> 400
    """
    orders = {
        '1': {
            'count': 1,
            "name": 'Tea',
            "price": 10,
            "item_final_price": 10
        }
    }
    client.set_cookie('localhost', 'orders', json.dumps(orders))
    response = client.post(url_for('landing.cart'))

    assert response.status_code == 400
    assert b"Request Body is not provided" in response.data


def test_post_cart_request_body_args(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (POST) with bad body arguments
      THEN check the response is valid -> 400
    """

    data = {'totalPrice': '4', 'finalPrice': 'test'}
    response = client.post(url_for('landing.cart'), data=data)

    assert response.status_code == 400
    assert b'Invalid Type for total price or final price' in response.data


@pytest.mark.skip
def test_post_cart_request_with_no_table_id_should_fail(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (POST) with no table id in cookies
      THEN check the response is valid -> 400
    """
    orders = {
        '1': {
            'count': 1,
            "name": 'Tea',
            "price": 10,
            "item_final_price": 10
        }
    }
    client.set_cookie('localhost', 'orders', json.dumps(orders))
    data = {'totalPrice': 4, 'finalPrice': 4}
    response = client.post(url_for('landing.cart'), data=data)

    assert response.status_code == 400
    assert b'Table id is not Provided in cookies' in response.data


def test_post_cart_with_non_exist_item_should_fail(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (POST) with non exist menu item
      THEN check the response is valid -> 400
    """
    new_table = Table(capacity=4, position='any', status=False)
    new_table.create()
    orders = {
        '1': {
            'count': 1,
            "name": 'Tea',
            "price": 10,
            "item_final_price": 10
        }
    }
    client.set_cookie('localhost', 'orders', json.dumps(orders))
    client.set_cookie('localhost', 'table_id', str(new_table.id))
    client.set_cookie('localhost', 'receipt', 'pending')
    data = {'totalPrice': 4, 'finalPrice': 4}
    response = client.post(url_for('landing.cart'), data=data)
    assert b'Invalid Menu Item!' in response.data
    assert response.status_code == 400


def test_post_cart_with_correct_parameters_should_succeed(client, init_db):
    """
      GIVEN a Flask application and database session
      WHEN the '/cart' page is requested (POST) with correct parameters
      THEN check the response is valid -> 200 and all cookies set and models created in database
    """
    # create models
    new_table = Table(capacity=4, position='any', status=False)
    new_table.create()
    category = Category(category_name='drink')
    category.create()
    new_menuitem = MenuItem(
        name='tea',
        price=10,
        serving_time_period='all',
        estimated_cooking_time=2,
        category_id=category.id
    )
    new_menuitem.create()
    # create cookies
    orders = {
        str(new_menuitem.id): {
            'count': 2,
            "name": new_menuitem.name,
            "price": new_menuitem.price,
            "item_final_price": new_menuitem.final_price()
        }
    }

    client.set_cookie('localhost', 'orders', json.dumps(orders))
    client.set_cookie('localhost', 'table_id', str(new_table.id))
    client.set_cookie('localhost', 'receipt', 'pending')
    data = {'totalPrice': new_menuitem.price, 'finalPrice': new_menuitem.final_price()}
    response = client.post(url_for('landing.cart'), data=data, follow_redirects=True)

    assert response.status_code == 200
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # check that response of redirect
    assert response.history[0].status_code == 302
    assert response.request.path == '/home'

    # check created receipt in database

    receipt = Receipt.query.get(1)
    assert receipt.table_id == new_table.id
    assert receipt.is_paid == True
    assert receipt.final_price == new_menuitem.final_price()
    assert receipt.total_price == new_menuitem.price
    # check created orders in database
    assert Order.query.count() == 1
    order = Order.query.get(1)
    assert order.count == orders[str(new_menuitem.id)]['count']
    assert order.menu_item_id == new_menuitem.id
    assert order.receipt_id == receipt.id
    assert order.status_code_id == 2
    # check cookies after redirect
    cookies = response.request.cookies
    assert cookies.get('receipt') == 'paid'
    assert cookies.get('receipt_id') == str(receipt.id)
    assert 'orders' not in cookies
