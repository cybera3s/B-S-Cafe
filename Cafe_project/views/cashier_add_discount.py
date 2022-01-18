from flask import render_template, request, redirect, flash, url_for
from database.manager import db
from models.models import Discount
from views.get_current_user import get_current_user


def cashier_new_discount():
    # route protecting
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    data = {
        'user': user,

    }
    if request.method == "GET":
        return render_template("cashier/cashier_add_discount.html", data=data)
    elif request.method == "POST":
        disValue = request.form['persentDiscount']
        status = None
        newDiscount = Discount(value=int(disValue))
        try:
            db.create(newDiscount)
            msg = "discount successfully added!"
            status = "success"
        except Exception as e:
            msg = "The entered value is Duplicated!"
            status = "danger"
        flash(msg, status)
        return redirect(request.url)