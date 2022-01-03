from flask import url_for, request, redirect, render_template

base_variables = {
    "page": {
        "base_title": "Cafe Maktab",
        "lang": 'en-US',
        "title": ''
    },
    "links": ["home", "menu", "orders"]
}


def index():
    data = base_variables
    data['page']['title'] = ['Home']
    if request.method == 'GET':
        data["title"] = 'home'
        return render_template("index.html", data=data)


def menu():
    data = base_variables
    data['page']['title'] = 'Menu'
    if request.method == 'GET':
        data["title"] = 'menu'
        return ' Menu Page ! '


def order(table_id):
    data = base_variables
    data['page']["title"] = 'Order'
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
