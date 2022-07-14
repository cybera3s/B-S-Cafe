import flask
from flask import request, render_template, redirect, url_for, Response, jsonify
from database.manager import db
from models import models
from models.models import Order

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


def menu():
    discounts = db.read_all(models.Discount)
    data = base_variables
    data["current_page"] = "menu"
    items = db.read_all(models.MenuItems)
    if request.method == "GET":
        data["title"] = "menu"
        return render_template("landing/menu.html", items=items, data=data, discounts=discounts)


def order(table_id):
    data = base_variables
    data["current_page"] = "order"
    items = db.read_all(models.MenuItems)
    discounts = db.read_all(models.Discount)

    if request.method == "POST":
        data = request.form or request.get_json()

        # table selecting
        if data.get('action') == 'select_table':
            response = flask.make_response(
                render_template("landing/order.html", data=data, items=items, discounts=discounts)
            )
            table = db.find_by(models.Table, id=table_id, status=False)
            if table is None:
                return Response("Table is Busy", status=400)

            receipt = db.find_by(models.Receipt, table_id=table_id, is_paid=False)
            # if receipt is already exists
            print(models.Order.next_id(db))
            if receipt is not None:
                receipt_id = receipt.id
            else:
                # create new receipt
                new_receipt = models.Receipt(int(table_id))
                receipt_id = db.create(new_receipt)

            response.headers['receipt_id'] = receipt_id
            return response

        # Add To Cart
        elif data.get('action') == 'add_to_cart':
            receipt_id = request.cookies.get('receipt_id')
            # current_receipt = db.read(models.Receipt, receipt_id)
            # if order already exists
            menu_item_id = data.get('itemId')
            existing_order = db.find_by(Order, receipt_id=receipt_id, menu_item_id=menu_item_id)
            item_count = data.get('itemCount')

            if existing_order:
                existing_order.count += item_count
                db.update(existing_order)

                return {
                    'status': 200,
                    'msg': 'item updated successfully'
                }

            # create new order
            new_order = models.Order(
                menu_item_id=menu_item_id,
                receipt_id=data.get('receiptId'),
                status_code_id=1,
                count=item_count
            )
            db.create(new_order)

            return {
                'status': 201,
                'msg': 'Added to cart successfully'
            }


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


def contact_us():
    data = base_variables
    data["current_page"] = "contact_us"
    if request.method == "GET":
        return render_template("landing/contact_us/contact_us.html", data=data)
