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
    data['page']['title'] = 'home'
    if request.method == 'GET':
        data["title"] = 'home'
        return render_template("index.html", data=data)


def menu():
    data = base_variables
    data["page"]["title"] = "menu"
    items = db.read_all(MenuItems)
    if request.method == 'GET':
        data["title"] = 'menu'
        return render_template('menu.html', items=items, data=data)


def order(table_id):
    data = base_variables
    data['page']["title"] = 'order'
    if request.method == 'GET':
        return f'GET/Order Page !{table_id} '
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
    return 'this is contact us page'