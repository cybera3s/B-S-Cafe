from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Discount, MenuItems, Category
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images/items'


def cashier_add_item():
    discount = db.read_all(Discount)
    category = db.read_all(Category)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        image_url = filename
        name = request.form['name']
        price = request.form['price']
        serving_time_period = request.form['serving']
        estimated_cooking_time = request.form['estimated']
        discount_id = request.form['discount']
        category_id = request.form['category']
        new_item = MenuItems(name=name, price=price, category_id=category_id, serving_time_period=serving_time_period,
                             estimated_cooking_time=estimated_cooking_time, picture_link=image_url,
                             discount_id=discount_id)

        db.create(new_item)
        flash('Image successfully uploaded and displayed below')
        return redirect(request.url)
    return render_template("cashier/cashier_add_item.html", discounts=discount, categorys=category)
