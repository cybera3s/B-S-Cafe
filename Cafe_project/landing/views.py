import json
from flask import request, render_template, redirect, url_for, Response, jsonify, make_response, Request
# local imports
from database.manager import db
from models import models

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
    tables = db.read_by(models.Table, ("status", "FALSE"))  # read tables that are empty
    serialized_tables = list(map(lambda t: vars(t), tables))
    return jsonify(serialized_tables)


def index():
    data = base_variables
    data["current_page"] = "index"
    tables = db.read_by(models.Table, ("status", "FALSE"))  # read tables that are empty

    if request.method == "GET":
        data["title"] = "home"
        return render_template("landing/index.html", data=data, tables=tables)


def home():
    data = base_variables
    data["current_page"] = "index"
    tables = db.read_by(models.Table, ("status", "FALSE"))  # read tables that are empty

    context = {
        'data': data,
        'tables': tables
    }
    if request.method == "GET":
        return render_template("landing/home/home.html", **context)


# TODO: Refactor here
def menu():
    discounts = db.read_all(models.Discount)
    data = base_variables
    data["current_page"] = "menu"
    items = db.read_all(models.MenuItems)
    if request.method == "GET":
        data["title"] = "menu"
        return render_template("landing/menu.html", items=items, data=data, discounts=discounts)


def order(table_id):

    # table selecting
    if request.method == "GET":

        return table_select(table_id)

    elif request.method == "POST":
        data = request.get_json()

        # Add To Cart
        if data.get('action') == 'add_to_cart':
            return add_to_cart(request)


def table_select(table_id) -> Response:
    data = base_variables
    data["current_page"] = "order"
    items = db.read_all(models.MenuItems)
    discounts = db.read_all(models.Discount)
    response = make_response(render_template("landing/order.html", data=data, items=items, discounts=discounts))
    # check if table is empty
    table = db.find_by(models.Table, id=table_id, status=False)
    if not table:
        return Response("Table is Busy", status=400)

    cookie_receipt = request.cookies.get('receipt')
    receipt = db.find_by(models.Receipt, table_id=table_id, is_paid=False)

    if not cookie_receipt:
        response.set_cookie('receipt', 'pending')

    # if receipt is already exists
    # print(models.Order.next_id(db))
    if receipt is not None:
        receipt_id = receipt.id
    else:
        # create new receipt
        new_receipt = models.Receipt(int(table_id))
        receipt_id = db.create(new_receipt)

    response.headers['receipt_id'] = receipt_id
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
    # 3
    if not item_count or not menu_item_id:
        return Response("menu item id or count not provided!", status=400)

    response = make_response({'msg': 'ok'})  # 4
    receipt_id = request.cookies.get('receipt_id')  # 5
    # 6
    if not receipt_id:
        return Response("Receipt id is not in cookies", status=400)

    cookie_receipt = request.cookies.get(str(receipt_id))  # 7
    # 8
    if cookie_receipt:
        orders = json.loads(cookie_receipt)  # 9
        # 10
        if orders.get(str(menu_item_id)):
            orders[str(menu_item_id)]['count'] += item_count
        else:  # 11
            orders[str(menu_item_id)] = {"count": item_count}
    # 12
    else:
        orders = {menu_item_id: {'count': item_count}}

    dumped_orders = json.dumps(orders)  # 13
    response.set_cookie(str(receipt_id), dumped_orders)  # 14
    return response


def cart():
    if request.method == "GET":
        # show cart items

        receipt_id = request.args.get("receipt_id")  # read request queries

        receipt_obj = db.read(models.Receipt, int(receipt_id))
        orders = receipt_obj.get_orders(db)
        total_price, final_price = receipt_obj.price(db)

        return render_template(
            "landing/cart.html", orders=orders, total_price=total_price, final_price=final_price
        )
    elif request.method == "POST":
        cookie = request.get_json()
        table_id = int(cookie["table"])
        receipt_id = int(cookie["receipt"])
        current_table = db.read(models.Table, table_id)
        current_receipt = db.read(models.Receipt, receipt_id)
        current_receipt.is_paid = True
        current_table.status = True
        db.update(current_receipt)
        db.update(current_table)
        return redirect(url_for("home"))


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
