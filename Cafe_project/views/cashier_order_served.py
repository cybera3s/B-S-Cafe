from datetime import date

from flask import url_for, request, redirect, render_template
from database.manager import db
from models import models
from models.models import Order, MenuItems, Receipt
from views.landing_views import base_variables


# Cashier
def cashier_order_served():
    data = base_variables
    data["page"]["title"] = "Served orders"
    items = db.read_by(Order, ('status_id', 3))
    for i in items:
        x = db.read(MenuItems, i.menu_item)
        i.menu_item = x.name
        i.create_time = i.create_time.strftime("%Y/%-m/%d  %-I:%m ")
    return render_template('cashier/Cashier_order_served.html', items=items, data=data)
