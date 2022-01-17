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
        menu_items = db.read_all(MenuItems)
        status = db.read_all(Status)
        status = db.read_all(Status)
        order = db.read_all(Order)
        request_data = request.get_json()
        if request_data['view'] == 'receipt_req':
            orders = db.read_by(Order, ('receipt_id', request_data['receipt']))
            return render_template('cashier/receipt-modify.html', orders=orders, items=menu_items, status=status)
        elif request_data['view'] == 'status_req':
            receipt_id = request_data['order']
            status_id = request_data['status_id']
            read_order = db.read(Order, receipt_id)
            read_order.status_id = int(status_id)
            db.update(read_order)
            return render_template('cashier/receipt-modify.html', orders=order, items=menu_items, status=status)

