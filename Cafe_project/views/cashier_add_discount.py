from flask import render_template, request, redirect, flash, url_for
from database.manager import db
from models.models import Discount


def cashier_new_discount():
    # route protecting
    user_email = request.cookies.get('user')
    if not user_email:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template("cashier/cashier_add_discount.html")
    elif request.method == "POST":
        disValue = request.form['persentDiscount']
        status = None
        newDiscount = Discount(value=int(disValue))
        try:
            db.create(newDiscount)
            msg = "discount successfully added!"
            status = "success"
        except Exception as e :
            msg = "The entered value is Duplicated!"
            status = "danger"
        flash(msg, status)
        return redirect(request.url)