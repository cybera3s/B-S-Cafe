from datetime import date

from flask import url_for, request, redirect, render_template
from database.manager import db
from models import models
from models.models import Order, MenuItems, Receipt
from views.landing_views import base_variables


def cashier_new_order():
    data = base_variables
    data["page"]["title"] = "New Orders"
    items = db.read_by(Order, ('status_id', 1))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_served.html', items=items, data=data)


def cashier_cook_order():
    data = base_variables
    data["page"]["title"] = "Cooking Orders"
    items = db.read_by(Order, ('status_id', 1))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_served.html', items=items, data=data)


def cashier_delete_order():
    data = base_variables
    data["page"]["title"] = "Delete Orders"
    items = db.read_by(Order, ('status_id', 1))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_served.html', items=items, data=data)


def cashier_paid_order():
    data = base_variables
    data["page"]["title"] = "Paid Orders"
    items = db.read_by(Order, ('status_id', 1))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_served.html', items=items, data=data)
