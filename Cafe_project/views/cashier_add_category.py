from flask import url_for, request, redirect, render_template, make_response

from database import manager
from database.manager import db
from models import models
from models.models import Order
base_variables ={
    "pages": {
        "home": {
            'title': 'خانه',
            'endpoint': 'home'
        },
        "menu": {
            'title': 'منو',
            'endpoint': 'menu'
        },
        "about_us": {
            'title': 'درباره ما',
            'endpoint': 'about_us'
        },
        "contact_us": {
            'title': 'ارتباط با ما',
            'endpoint': 'contact_us'
        },
    },
    "current_page": ''
}


# Cashier
def cashier_add_category():

    items_category = db.read_all(models.Category)
    items_discount = db.read_all(models.Discount)
    if request.method == 'GET':
        return render_template('cashier/cashier_add_category.html', items_category=items_category,
                               items_discount=items_discount)
    elif request.method == "POST":
        name = request.form.get('name')
        root = request.form.get('root')
        discount = request.form.get('discount')
        print(name, root, discount)
        category = models.Category(name, root)
        db.create(category)
        resp = make_response(redirect(url_for('cashier_add_category')))
        return resp
