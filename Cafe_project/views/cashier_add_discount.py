from flask import render_template, request, redirect, flash
from database.manager import db
from models.models import Discount


def cashier_new_discount():
    if request.method == "GET":
        return render_template("cashier/cashier_add_discount.html")
    elif request.method == "POST":
        disValue = request.form['persentDiscount']

        newDiscount = Discount(value=int(disValue))

        db.create(newDiscount)
        flash("Discount successfuly added!")
        return redirect(request.url)