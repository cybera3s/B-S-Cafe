from flask import render_template


def cashier_table():
    data = {
        "page": {
            "title": "tables",
        },
    }

    return render_template('cashier/tables.html', data=data)
