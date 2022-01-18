from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Discount, Category, MenuItems


def cashier_list_menu():

    menuitem = db.read_all(MenuItems)
    discount = db.read_all(Discount)
    category = db.read_all(Category)
    if request.method == 'GET':
        return render_template('cashier/cashier_list_menu.html', menuitems=menuitem)
    if request.method == 'POST':
        request_data = request.get_json()
        if request_data['view'] == 'item':
            print(request_data)
            print(request_data['view'])
            items = db.read_by(MenuItems, ('id', request_data['items']))
            return render_template('cashier/item-modify.html', items=items, categories=category, discounts=discount)

        elif request_data['view'] == 'list_item':
            print(request_data)
            print(request_data['name'])
            id = request_data['id']
            name = request_data['name']
            price = request_data['price']
            serving_time = request_data['serving_time']
            estimated = request_data['estimated']
            discount_value = int(request_data['discount'])
            discount_id = list(filter(lambda d: d.value == discount_value, discount))[0].id
            category_name = request_data['category']
            category_id = list(filter(lambda c: c.category == category_name, category))[0].id
            item_update = db.read(MenuItems, id)
            item_update.price = int(price)
            item_update.serving_time_period = int(serving_time)
            item_update.estimated_cooking_time = int(estimated)
            item_update.picture_link = int(estimated)
            item_update.discount_id = int(discount_id)
            item_update.category_id = int(category_id)
            db.update(item_update)
            return render_template('cashier/cashier_list_menu.html', menuitems=menuitem)
