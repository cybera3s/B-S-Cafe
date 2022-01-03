from flask import url_for, request, redirect, render_template

data = {
    "links": ['Home', 'Menu', 'Order', 'Contact Us', 'About Us']
}

def index():
    if request.method == 'GET':
        data["title"] = 'home'
        return render_template("index.html", data=data)


def menu():
    if request.method == 'GET':
        data["title"] = 'menu'
        return ' Menu Page ! '


def order(table_id):
    data["title"] = 'home'
    if request.method == 'GET':
        return f'GET/Order Page !{table_id} '
    elif request.method == 'POST':
        return f'POST/Order Page !{table_id} '
    elif request.method == 'DELETE':
        return f'DELETE/Order Page !{table_id}'

def about_us():
    if request.method == 'GET':
        return render_template('about_us.html', data=data)