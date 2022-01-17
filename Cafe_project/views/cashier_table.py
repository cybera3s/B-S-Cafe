from flask import render_template, request
from database.manager import db
from models.models import Table

def cashier_table():
    data = {
        "page": {
            "title": "tables",
        },
    }

    return render_template('cashier/tables.html', data=data)
