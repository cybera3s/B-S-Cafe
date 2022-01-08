from flask import url_for, request, redirect, render_template
from database.manager import db
from models.models import Order
from views.landing_views import base_variables


# Cashier
def cashier_order_served():
    data = base_variables
    data["page"]["title"] = "served"
    items = db.read_by(Order, ('status_code', 3))
    if request.method == 'GET':
        data["title"] = 'served'
        return render_template('Cashier/Cashier_order_served.html', items=items, data=data)
