from flask import url_for, request, redirect, render_template
from manager import DBManager
from models import *

base_variables = {
    "page": {
        "base_title": "Cafe Maktab",
        "lang": 'en-US',
        "title": ''
    },
    "links": ["home", "menu", "about_us", "contact_us"]
}
db = DBManager()


def index():
    data = base_variables
    tables = db.read_all(Table)
    data['page']['title'] = 'home'
    if request.method == 'GET':
        data["title"] = 'home'
        return render_template("index.html", data=data, tables=tables)


def menu():
    data = base_variables
    data["page"]["title"] = "menu"
    items = db.read_all(MenuItems)
    if request.method == 'GET':
        data["title"] = 'menu'
        return render_template('menu.html', items=items, data=data)


def order(table_id):
    data = base_variables
    items = db.read_all(MenuItems)
    table = db.read(Table, table_id)
    data['page']["title"] = 'order'
    if request.method == 'GET':
        if table.status:
            table.status = False
        else:
            table.status = True
        db.update(table)
        return render_template('order.html', data=data, items=items)
    elif request.method == 'POST':
        return f'POST/Order Page !{table_id} '
    elif request.method == 'DELETE':
        return f'DELETE/Order Page !{table_id}'


def about_us():
    data = base_variables
    data['page']['title'] = 'About Us'
    if request.method == 'GET':
        return render_template('about_us.html', data=data)


def contact_us():
    data = base_variables
    data['page']['title'] = 'About Us'
    if request.method == 'GET':
