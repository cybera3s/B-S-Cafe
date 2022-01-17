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
    }

    return render_template('cashier/tables.html', data=data)
