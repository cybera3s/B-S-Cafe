from flask import request, render_template, flash, redirect, url_for
from database.manager import db
from models import models


def cashier_add_category():
    # route protecting
    user_email = request.cookies.get('user')
    if not user_email:
        return redirect(url_for('login'))

    items_category = db.read_all(models.Category)
    items_discount = db.read_all(models.Discount)
    if request.method == 'GET':
        return render_template('cashier/cashier_add_category.html', items_category=items_category,
                               items_discount=items_discount)

    elif request.method == "POST":

        category = request.form.get('category')
        root_id = request.form.get('root_id')
        discount_id = int(request.form.get('discount_id'))

        new_category = models.Category(category, root_id, discount_id)
        db.create(new_category)

        flash('New Category Added !')
        return render_template('cashier/cashier_add_category.html', items_category=items_category,
                               items_discount=items_discount)
