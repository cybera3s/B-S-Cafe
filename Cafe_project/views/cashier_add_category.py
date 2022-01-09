from flask import url_for, request, redirect, render_template, make_response

from database import manager
from database.manager import db
from models import models
from models.models import Order
from views.landing_views import base_variables


# Cashier
def cashier_add_category():
    data = base_variables
    data["page"]["title"] = "category"
    items_category = db.read_all(models.Category)
    items_discount = db.read_all(models.Category)
    if request.method == 'GET':
        data["title"] = 'category'
        return render_template('cashier/cashier_add_category.html', items_category=items_category, data=data,
                               items_discount=items_discount)
    elif request.method == "POST":
        name = request.form.get('name')
        root = request.form.get('root')
        discount = request.form.get('discount')
        print(name, root, discount)
        # category = models.Category(name, root)
        # db.create(category)
        resp = make_response(redirect(url_for('cashier_add_category')))
        return resp
