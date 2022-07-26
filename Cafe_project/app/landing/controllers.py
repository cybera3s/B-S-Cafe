import json
from flask import request, render_template, redirect, url_for, Response, jsonify, make_response, Request, abort

from app.models import *

base_variables = {
    "pages": {
        "home": {"title": "Home", "endpoint": "home"},
        "menu": {"title": "Menu", "endpoint": "menu"},
        "about_us": {"title": "About", "endpoint": "about_us"},
        "contact_us": {"title": "Contact Us", "endpoint": "contact_us"},
    },
    "current_page": "",
    "site_name": "Bitter & Sweet"
}


def available_tables():
    """
        return serialized free tables on get request
    """
    tables = Table.query.filter(status, False).all()  # read tables that are empty
    serialized_tables = list(map(lambda t: vars(t), tables))
    return jsonify(serialized_tables)


def index():
    data = base_variables
    data["current_page"] = "index"
    tables = Table.query.filter(Table.status == False).all()  # read tables that are empty
    context = {
        'data': data,
        'tables': tables
    }
    if request.method == "GET":
        data["title"] = "home"
        return render_template("landing/index.html", **context)


def home():
    data = base_variables
    data["current_page"] = "index"
    tables = Table.query.filter(Table.status == False).all()  # read tables that are empty

    context = {
        'data': data,
        'tables': tables
    }
    if request.method == "GET":
        return render_template("landing/home/home.html", **context)


def set_final_price(item):
    item.final_price = item.final_price(db)
    return item


def menu():
    """
        show menu items on GET request
    """
    discounts = Discount.query.all()
    data = base_variables
    data["current_page"] = "menu"
    items = MenuItem.query.all()
    modified_items = map(set_final_price, items)

    if request.method == "GET":
        data["title"] = "menu"
        context = {
            'items': modified_items,
            'data': data,
            'discounts': discounts
        }
        return render_template("landing/menu.html", **context)


def order(table_id: int):
    """
        select table on GET request
        add to cart on POST request
    """
    # table selecting
    if request.method == "GET":
        return table_select(table_id)

    # Add To Cart
    elif request.method == "POST":
        return add_to_cart(request)


def table_select(table_id: int) -> Response:
    """
       if table is free and receipt is pending in cookies then returns
       response with table id as cookie
       else if table is full returns 400 response

    """
    # get data from db for response
    data = base_variables
    data["current_page"] = "order"
    items = MenuItem.query.all()
    modified_items = map(set_final_price, items)

    discounts = Discount.query.all()
    context = {
        'data': data,
        'items': modified_items,
        'discounts': discounts
    }
    response = make_response(render_template("landing/order-index.html", **context))
    # check if table is empty
    table = Table.query.filter((Table.id == table_id) & (Table.status == False)).all()
    if not table:
        return Response("Table is Busy", status=400)

    cookie_receipt = request.cookies.get('receipt')
    # if receipt is not pending then pend it
    if not cookie_receipt:
        response.set_cookie('receipt', 'pending')

    response.set_cookie('table_id', str(table_id))
    return response


def add_to_cart(request: Request) -> Response:
    """
        :param request : a flask request object\n
        :returns a Response object\n
        #1 : get json data\n
        #2 : get menu item id and count of that from data -> int, int\n
        #3 : if menu item id and count is None returns Bad Request Response\n
        #4 : set default response json -> Response, 200 OK\n
        #5 : get receipt id from cookies -> str\n
        #6 : if receipt id from cookies is none then return Bad Request response\n
        #7 : get orders of corresponding receipt id from cookies -> json or None\n
        #8 : check if orders of receipt id exist in cookies then -> #9 , #10, #11\n
        #9 : deserialize json orders from receipt -> orders: dict\n
        #10 : if menu item id exist in orders then add count of existing item with item_count in orders\n
        #11 : create new menu item id key with item_count as value in orders\n
        #12 : orders of receipt id does NOT exist in cookies then create new orders -> dict\n
        #13 : json serialize orders
        #14 : set receipt_id as key in cookies with serialized orders as value
    """
    data = request.get_json()  # 1
    # 2
    menu_item_id = data.get('itemId')
    item_count = data.get('itemCount')
    item_name = data.get('itemName')
    item_price = data.get('itemPrice')
    item_final_price = data.get('finalPrice')
    # 3
    if not item_count or not menu_item_id:
        return Response("menu item id or count not provided!", status=400)

    response = make_response({'msg': 'ok'})  # 4
    receipt = request.cookies.get('receipt')  # 5
    # 6
    if not receipt:
        return Response("You have no Receipt yet!", status=400)

    cookie_orders = request.cookies.get('orders')  # 7
    # 8
    if cookie_orders:
        orders = json.loads(cookie_orders)  # 9
        # 10
        if orders.get(str(menu_item_id)):
            orders[str(menu_item_id)]['count'] += item_count
        else:  # 11
            orders[str(menu_item_id)] = {
                "count": item_count,
                "name": item_name,
                "price": item_price,
                "item_final_price": item_final_price
            }
    # 12
    else:

        orders = {
            menu_item_id: {
                'count': item_count,
                "name": item_name,
                "price": item_price,
                "item_final_price": item_final_price
            }
        }

    dumped_orders = json.dumps(orders)  # 13
    response.set_cookie('orders', dumped_orders)  # 14
    return response


def cart():
    """
        GET request: get orders from cookies
        POST request: complete payment
    """
    # get orders of cart
    if request.method == "GET":
        # show cart items
        cookie_orders = request.cookies.get('orders')
        if not cookie_orders:
            return Response("There is no orders", status=400)

        orders = json.loads(cookie_orders)
        if orders:
            orders = orders.values()

        total_price = 0
        final_price = 0

        for o in orders:
            total_price += o['count'] * o['price']
            final_price += o['count'] * (o['item_final_price'] or o['price'])

        context = {
            'orders': orders,
            'total_price': total_price,
            'final_price': final_price
        }
        return render_template("landing/cart.html", **context)

    # payment
    elif request.method == "POST":
        data = request.form
        total_price = data.get('totalPrice')
        final_price = data.get('finalPrice')
        receipt = request.cookies.get('receipt')
        table_id = request.cookies.get('table_id')
        orders = request.cookies.get('orders')

        if not total_price or not final_price:
            return Response("total price or final price is not provided", status=400)

        current_table = Table.query.filter((Table.id == table_id) & (Table.status == False)).first()
        if not current_table:
            return Response("Table is not empty, try Another Table", status=400)
        if not receipt:
            return Response("You have no Receipt yet!", status=400)
        if not orders:
            return Response("You have no Orders yet!", status=400)

        orders = json.loads(orders)
        # register Receipt
        receipt = Receipt(table_id=int(table_id))
        receipt.is_paid = True
        receipt.total_price = total_price
        receipt.final_price = final_price
        receipt_id = receipt.create()

        # register order objects
        for item_id, detail in orders.items():
            order_obj = models.Order(
                menu_item_id=item_id,
                status_code_id=2,
                count=detail['count'],
                receipt_id=receipt_id.id
            )
            order_obj.create()

        # update and save table status
        current_table.status = True
        db.session.commit()
        # prepare response and delete old cookies
        response = make_response(redirect(url_for(".home")))
        response.set_cookie('receipt', 'paid')
        response.set_cookie('receipt_id', str(receipt_id))
        response.delete_cookie('orders')

        return response


def about_us():
    data = base_variables
    data["current_page"] = "about_us"
    if request.method == "GET":
        return render_template("landing/about_us/about_us.html", data=data)


# TODO: add functionality to contact_us form
def contact_us():
    data = base_variables
    data["current_page"] = "contact_us"
    if request.method == "GET":
        return render_template("landing/contact_us/contact_us.html", data=data)
