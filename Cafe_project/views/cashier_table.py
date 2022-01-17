import json

from flask import render_template, request
from database.manager import db
from models.models import Table, Receipt


def cashier_table():
    tables = db.read_all(Table)  # fetch all of tables from database

    # turn status of boolean to string
    for table in tables:
        table.status = 'Busy' if table.status else 'Free'

    data = {
        "page": {
            "title": "tables",
        },
        "content": {
            "tables": tables,
        }
    }

    # handle AJAX POST request for changing state of tables
    if request.method == "POST":
        received_data = request.get_json()
        id = received_data['id']

        if received_data['get_info']:   # Handle show info section
            orders = Table.current_orders(db, id)
            return render_template('cashier/table_items.html', data=data, orders=orders)
        else:
            table = db.read(Table, id)
            table.status = False
            db.update(table)
            return '200'
    # handle get request
    return render_template('cashier/tables.html', data=data)
