from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Order, Receipt


def cashier_order():
    orders = db.read_all(Order)
    receipts = db.read_all(Receipt)

    return render_template('cashier/order.html', orders=orders, receipts=receipts)
