from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Order, Receipt, MenuItems, Status


def cashier_order():
    if request.method == 'GET':
        receipts = db.read_all(Receipt)
        for i in receipts:
            i.create_time = i.create_time.strftime("%Y/%-m/%d %-I:%m ")
        return render_template('cashier/order.html', receipts=receipts)
    if request.method == 'POST':
        request_data = request.get_json()
        orders = db.read_by(Order, ('receipt_id', request_data['receipt']))
        menu_items = db.read_all(MenuItems)
        status = db.read_all(Status)
        for i in status:
            print(i.status)
        return render_template('cashier/receipt-modify.html', orders=orders, items=menu_items, status=status)


