from flask import render_template, request
from database.manager import db
from models.models import Table


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
        data = request.get_json()
        id = data['id']
        table = db.read(Table, id)
        table.status = False
        db.update(table)
        return '200'

    return render_template('cashier/tables.html', data=data)
