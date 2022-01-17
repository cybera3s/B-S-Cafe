from flask import url_for, request, redirect, render_template, flash
from database.manager import DBManager, db
from models.models import Discount, Category, MenuItems


def cashier_list_menu():
    request_data = request.get_json()
    menuitem = db.read_all(MenuItems)
    discount = db.read_all(Discount)
    category = db.read_all(Category)
    if request.method == 'GET':
        return render_template('cashier/cashier_list_menu.html', menuitems=menuitem)
    if request.method == 'POST':
        if request_data['view'] == 'item':
            items = db.read_by(MenuItems, ('id', request_data['items']))
            return render_template('cashier/item-modify.html', items=items, categories=category, discounts=discount)
