from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Order, Receipt, MenuItems


def cashier_order():
    if request.method == 'GET':
        receipts = db.read_all(Receipt)
        return render_template('cashier/order.html', receipts=receipts)
    if request.method == 'POST':
        request_data = request.get_json()
        orders = db.read_by(Order, ('receipt_id', request_data['receipt']))
        menu_items = db.read_all(MenuItems)
        return render_template('cashier/receipt-modify.html', orders=orders, items=menu_items)


