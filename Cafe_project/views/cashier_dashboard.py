from flask import url_for, request, redirect, render_template, make_response, flash
from database.manager import db
from models import models


def cashier_dashboard():
    today_customer_count = db.read_all(models.Receipt)
    print(today_customer_count)
    print(today_customer_count.sort(key=lambda o: o.create_time))

    return render_template('cashier/dashboard.html', customer_count=len(today_customer_count))
