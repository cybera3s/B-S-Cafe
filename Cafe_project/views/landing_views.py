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
    data = base_variables
    data['current_page'] = 'menu'
    items = db.read_all(models.MenuItems)
    if request.method == 'GET':
        data["title"] = 'menu'
        return render_template('menu.html', items=items, data=data)


def order(table_id):
    data = base_variables
    data['current_page'] = 'order'
    items = db.read_all(models.MenuItems)
    table = db.read(models.Table, table_id)

    if request.method == 'GET':
        res = flask.make_response(render_template('order.html', data=data, items=items))
        new_receipt = models.Receipt({}, int(table_id))
        receipt_id = db.create(new_receipt)
        res.set_cookie('receipt_id', str(receipt_id))
        res.set_cookie('table_id', table_id)
        return res
    elif request.method == 'POST':
        data = request.get_json()
        value1 = data['order']['item_id']
        value2 = data['order']['count']
        table = data['table']
        receipt = data['receipt']
        print(f"""
        item_id : {value1}
        count : {value2}
        receipt_id : {receipt}
        table)id : {table}""")
        return '200'
    elif request.method == 'DELETE':
        return f'DELETE/Order Page !{table_id}'
    return

def cart():
    pass


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
