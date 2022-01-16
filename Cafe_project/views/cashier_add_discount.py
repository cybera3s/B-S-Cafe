from flask import render_template, request, redirect, flash
from database.manager import db
from models.models import Discount


def cashier_new_discount():
    if request.method == "GET":
        return render_template("cashier/cashier_add_discount.html")
    elif request.method == "POST":
        disValue = request.form['persentDiscount']

        newDiscount = Discount(value=int(disValue))
        try:
            db.create(newDiscount)
            msg = "discount successfully added!"
        except Exception as e :
            msg = "The entered value is Duplicated!"
        flash(msg)
        return redirect(request.url)