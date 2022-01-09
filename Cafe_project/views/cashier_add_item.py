from flask import url_for, request, redirect, render_template
# from app import photos
from database.manager import DBManager, db
from models.models import MenuItems


def cashier_add_item():
    if request.method == 'GET':
        return render_template('cashier/cashier_add_item.html')
    #
    # else:
    #     image_url = photos.url(photos.save((request.form['image'])))
    #     name = request.form['name']
    #     price = request.form['price']
    #     serving_time_period = request.form['serving']
    #     estimated_cooking_time = request.form['estimated']
    #     discount_id = request.form['discount']
    #     category_id = request.form['category']
    #     new_item = MenuItems(name=name, price=price, category_id=category_id, serving_time_period=serving_time_period,
    #                          estimated_cooking_time=estimated_cooking_time, picture_link=image_url,
    #                          discount_id=discount_id)
    #
    #     db.create(new_item)