import flask
from flask import url_for, request, redirect, render_template
import json
from database.manager import db
from models import models

base_variables = {
    "pages": {
        "home": {
            'title': 'خانه',
            'endpoint': 'home'
        },
        "menu": {
            'title': 'منو',
            'endpoint': 'menu'
        },
        "about_us": {
            'title': 'درباره ما',
            'endpoint': 'about_us'
        },
        "contact_us": {
            'title': 'ارتباط با ما',
            'endpoint': 'contact_us'
        },
    },
    "current_page": ''
}


def index():
    data = base_variables
    data['current_page'] = 'index'
    tables = db.read_all(models.Table)
    if request.method == 'GET':
        data["title"] = 'home'
        return render_template("index.html", data=data, tables=tables)


def home():
    data = base_variables
    data['current_page'] = 'index'
    if request.method == 'GET':
        return render_template("home.html", data=data)


def menu():
    discounts = db.read_all(models.Discount)
    data = base_variables
    data['current_page'] = 'menu'
    items = db.read_all(models.MenuItems)
    if request.method == 'GET':
        data["title"] = 'menu'
        return render_template('menu.html', items=items, data=data, discounts=discounts)


def order(table_id):
    data = base_variables
    data['current_page'] = 'order'
    items = db.read_all(models.MenuItems)
    table = db.read(models.Table, table_id)
    discounts = db.read_all(models.Discount)

    if request.method == 'GET':
        res = flask.make_response(render_template('order.html', data=data, items=items, discounts=discounts))
        new_receipt = models.Receipt(int(table_id))
        receipt_id = db.create(new_receipt)
        res.set_cookie('receipt_id', str(receipt_id))
        res.set_cookie('table_id', table_id)
        return res
    elif request.method == 'POST':
        cookie = request.get_json()
        item_id = cookie['order']['item_id']
        item_count = cookie['order']['count']
        table = cookie['table']
        receipt = cookie['receipt']
        new_order = models.Order(item_id, receipt, 1, int(item_count))
        order_id = db.create(new_order)
        current_receipt = db.read(models.Receipt, int(receipt))
        current_menu_item = db.read(models.MenuItems, new_order.menu_item)
        discount = db.read(models.Discount, current_menu_item.discount_id)
        current_receipt.total_price += current_menu_item.price * new_order.count
        if discount.id == 1:
            current_receipt.final_price += current_menu_item.price * new_order.count
        else:
            current_receipt.final_price += ((current_menu_item.price - ((current_menu_item.price * discount.value) / 100)) * new_order.count)
        current_receipt.orders.append(order_id)
        db.update(current_receipt)
        return '200'
    elif request.method == 'DELETE':
        pass


def cart():
    if request.method == 'GET':
        receipt = request.cookies.get('receipt_id')
        orders = db.read_by(models.Order, ('receipt_id', receipt))
        menu_items = db.read_all(models.MenuItems)
        current_receipt = db.read(models.Receipt, int(receipt))
        return render_template('cart.html', orders=orders, items=menu_items, receipt=current_receipt)
    if request.method == "POST":
        cookie = request.get_json()
        table_id = int(cookie['table'])
        receipt_id = int(cookie['receipt'])
        current_table = db.read(models.Table, table_id)
        current_receipt = db.read(models.Receipt, receipt_id)
        current_receipt.is_paid = True
        current_table.status = True
        db.update(current_receipt)
        db.update(current_table)
        return redirect(url_for('home'))


def about_us():
    data = base_variables
    data['current_page'] = 'about_us'
    if request.method == 'GET':
        return render_template('about_us.html', data=data)


def contact_us():
    data = base_variables
    data['current_page'] = 'contact_us'
    if request.method == 'GET':
        return render_template('contact_us.html', data=data)