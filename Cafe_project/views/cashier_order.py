from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Order


def cashier_order():
    order = db.read_all(Order)
    print(list(filter(lambda o: o.menu_item, order))[0].menu_item)
    return render_template('cashier/order.html')
