from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Discount, MenuItems, Category
import os
from werkzeug.utils import secure_filename
from views.get_current_user import get_current_user

UPLOAD_FOLDER = 'static/images/items'


def cashier_add_item():
    # route protecting
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    data = {
        'user': user,

    }
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
        discount_value = int(request.form['discount'])
        discount_id = list(filter(lambda d: d.value == discount_value, discount))[0].id
        category_name = request.form['category']
        category_id = list(filter(lambda c: c.category == category_name, category))[0].id
        new_item = MenuItems(name=name, price=price, category_id=category_id, serving_time_period=serving_time_period,
                             estimated_cooking_time=estimated_cooking_time, picture_link=image_url,
                             discount_id=discount_id)

        db.create(new_item)
        flash('Image successfully uploaded and displayed below')
        return redirect(request.url)
    return render_template("cashier/cashier_add_item.html", discounts=discount, categorys=category, data=data)
