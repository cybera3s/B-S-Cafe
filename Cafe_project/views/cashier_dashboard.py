from flask import url_for, request, redirect, render_template, make_response, flash
from database.manager import db
from models import models
from datetime import datetime


def cashier_dashboard():
    all_receipts = db.read_all(models.Receipt)

    today_receipts = list(filter(lambda order: order.create_time.day == datetime.now().day, all_receipts))
    today_earnings = list(map(lambda order))
    return render_template('cashier/dashboard.html', customer_count=len(today_receipts))
