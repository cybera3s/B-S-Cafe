from flask import url_for, request, redirect, render_template
from database.manager import db
from models.models import Order, MenuItems
from views.get_current_user import get_current_user

base_variables = {
    "page": {
        "lang": 'en-US',
        "title": ''
    },
}


def cashier_new_order():
    user = get_current_user()
    # route protecting
    if not user:
        return redirect(url_for('login'))

    data = base_variables
    data['user'] = user
    data["page"]["title"] = "New Orders"
    title_get = 'cashier_order_new'
    items = db.read_by(Order, ('status_id', 1))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_status.html', items=items, data=data, title_get=title_get)


def cashier_cook_order():
    user = get_current_user()
    # route protecting
    if not user:
        return redirect(url_for('login'))

    data = base_variables
    data["page"]["title"] = "Cooking Orders"
    data['user'] = user

    title_get = 'cashier_cook_order'
    items = db.read_by(Order, ('status_id', 2))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_status.html', items=items, data=data, title_get=title_get)


def cashier_order_served():
    user = get_current_user()
    # route protecting
    if not user:
        return redirect(url_for('login'))

    data = base_variables
    data['user'] = user
    data["page"]["title"] = "Served orders"
    title_get = 'cashier_order_served'
    items = db.read_by(Order, ('status_id', 3))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_status.html', items=items, data=data, title_get=title_get)


def cashier_delete_order():
    user = get_current_user()
    # route protecting
    if not user:
        return redirect(url_for('login'))

    data = base_variables
    data['user'] = user
    data["page"]["title"] = "Delete Orders"
    title_get = 'cashier_delete_order'
    items = db.read_by(Order, ('status_id', 4))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_status.html', items=items, data=data, title_get=title_get)


def cashier_paid_order():
    user = get_current_user()
    # route protecting
    if not user:
        return redirect(url_for('login'))

    data = base_variables
    data['user'] = user
    data["page"]["title"] = "Paid Orders"
    title_get = 'cashier_paid_order'
    items = db.read_by(Order, ('status_id', 5))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_status.html', items=items, data=data, title_get=title_get)
