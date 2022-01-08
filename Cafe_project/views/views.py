from flask import url_for, request, redirect, render_template
from database.manager import db
from models import models

base_variables = {
    "page": {
        "lang": 'en-US',
        "title": ''
    },
    "links": ["home", "menu", "about_us", "contact_us"]
}


def index():
    data = base_variables
    # tables = db.read_all(Table)
    data['page']['title'] = 'home'
    if request.method == 'GET':
        data["title"] = 'home'
        return "<h1>Test Runing...</h1>"
        # return render_template("index.html", data=data, tables=tables)


def menu():
    data = base_variables
    data["page"]["title"] = "menu"
    items = db.read_all(models.MenuItems)
    if request.method == 'GET':
        data["title"] = 'menu'
        return render_template('menu.html', items=items, data=data)


def order(table_id):
    data = base_variables
    items = db.read_all(models.MenuItems)
    table = db.read(models.Table, table_id)
    data['page']["title"] = 'order'
    if request.method == 'GET':
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
        return render_template('contact_us.html', data=data)
