from flask import url_for, request, redirect, render_template, make_response, flash
from database.manager import db
from models import models
from datetime import datetime, timedelta


def cashier_dashboard():
    # route protecting
    user_email = request.cookies.get('user')
    if not user_email:
        return redirect(url_for('login'))
    all_receipts = db.read_all(models.Receipt)

    today_receipts = list(filter(lambda order: order.create_time.day == datetime.now().day, all_receipts))
    today_earnings = sum(list(map(lambda order: order.final_price, today_receipts)))

    report = models.Receipt.last_week_report(all_receipts=all_receipts)

    user = db.read_by(models.Cashier, ('email', user_email))
    data = {
        'user': user[0],
        'today_earnings': today_earnings,
        'customer_count': len(today_receipts),

        'chart': {

            'labels': list(map(lambda i: i[1], report)),
            'sum_receipts': list(map(lambda i: i[0], report))

        }

    }

    if request.method == "POST":
        cashier = models.Cashier(**dict(request.form), id=user[0].id)
        db.update(cashier)
        data['user'] = cashier
        return render_template('cashier/dashboard.html', data=data)

    return render_template('cashier/dashboard.html', data=data)
