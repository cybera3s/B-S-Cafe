from models.models import *
from database.manager import db
from flask import url_for, request, redirect, render_template, make_response, flash, Response, Request, current_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from utility.utils import allowed_file

base_variables = {
    "page": {"lang": "en-US", "title": ""},
}


def save_and_validate_file(req: Request, key: str):
    """
        Takes request and a string key and look for key in
        request.files if found and be valid then save it to UPLOAD_FOLDER
        and returns filename
    """
    if key not in req.files:
        raise KeyError('No File Part')

    file = req.files[key]

    if file.filename == "":
        raise FileNotFoundError('No image selected for uploading!')

    # check if uploaded file has correct extensions and file is not none
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename


def get_current_user() -> Cashier:
    """
    return current Cashier object from database if exist in cookies
    """
    user_res = None

    if "user" in request.cookies:
        user = request.cookies["user"]
        user_res = db.read_by(Cashier, ("email", user))[0]

    return user_res


def login_required(view):
    """
        takes a view function and check if user is in cookies
    """

    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(url_for("login"))
        return view(user, *args, **kwargs)

    return wrapper


@login_required
def cashier_add_category(user):
    data = {
        "user": user,
    }
    items_category = db.read_all(Category)
    items_discount = db.read_all(Discount)

    context = {
        'items_category': items_category,
        'items_discount': items_discount,
        'data': data,
    }
    if request.method == "GET":
        return render_template("cashier/cashier_add_category.html", **context)

    elif request.method == "POST":

        category = request.form.get("category")
        root_id = request.form.get("root_id")
        discount_id = int(request.form.get("discount_id"))

        new_category = Category(category, root_id, discount_id)
        db.create(new_category)

        context = {
            'items_category': items_category,
            'items_discount': items_discount,
            'data': data,
        }
        flash("New Category Added !")
        return render_template("cashier/cashier_add_category.html", **context)


@login_required
def cashier_new_discount(user):

    data = {
        "user": user,
    }
    if request.method == "GET":
        return render_template("cashier/cashier_add_discount.html", data=data)
    elif request.method == "POST":
        disValue = request.form["persentDiscount"]
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


def cashier_add_item():
    # route protecting
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    data = {
        "user": user,
    }
    discount = db.read_all(Discount)
    category = db.read_all(Category)
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        image_url = filename
        name = request.form["name"]
        price = request.form["price"]
        serving_time_period = request.form["serving"]
        estimated_cooking_time = request.form["estimated"]
        discount_value = int(request.form["discount"])
        discount_id = list(filter(lambda d: d.value == discount_value, discount))[0].id
        category_name = request.form["category"]
        category_id = list(filter(lambda c: c.category_name == category_name, category))[0].id
        new_item = MenuItems(
            name=name,
            price=price,
            category_id=category_id,
            serving_time_period=serving_time_period,
            estimated_cooking_time=estimated_cooking_time,
            picture_link=image_url,
            discount_id=discount_id,
        )

        db.create(new_item)
        flash("Menu Item successfully Added !")
        return redirect(request.url)
    return render_template(
        "cashier/cashier_add_item.html",
        discounts=discount,
        categorys=category,
        data=data,
    )


@login_required
def cashier_dashboard(user):
    all_receipts = db.read_all(Receipt)

    today_receipts = list(
        filter(lambda order: order.created_at.day == datetime.now().day, all_receipts)
    )
    today_earnings = sum(list(map(lambda order: order.final_price, today_receipts)))

    report = Receipt.last_week_report(all_receipts=all_receipts)

    data = {
        "user": user,
        "today_earnings": today_earnings,
        "customer_count": len(today_receipts),
        "chart": {
            "labels": list(map(lambda i: i[1], report)),
            "sum_receipts": list(map(lambda i: i[0], report)),
        },
    }

    if request.method == "POST":
        cashier = Cashier(**dict(request.form), id=user.id)
        db.update(cashier)
        data["user"] = cashier
        return render_template("cashier/dashboard.html", data=data)

    return render_template("cashier/dashboard.html", data=data)


@login_required
def cashier_order(user):
    if request.method == "GET":
        receipts = db.read_all(Receipt)

        context = {
            "data": {
                "user": user
            },
            "receipts": receipts
        }

        return render_template("cashier/order.html", **context)

    if request.method == "POST":
        # get json payload of request
        request_data = request.get_json()

        context = {
            "status": db.read_all(Status),
        }

        # get receipt orders
        if request_data["view"] == "receipt_req":
            context['orders'] = Order.read_by_receipt_with_menu_items_status(request_data["receipt_id"], db)
            return render_template("cashier/receipt-modify.html", **context)

        # change order status of a receipt
        elif request_data["view"] == "status_req":
            receipt_id = request_data["order"]
            status_id = request_data["status_id"]
            read_order = db.read(Order, receipt_id)
            read_order.status_code_id = int(status_id)
            db.update(read_order)
            return render_template(
                "cashier/receipt-modify.html",
                **context
            )


@login_required
def cashier_order_status(user, status_id):
    data = base_variables
    data["user"] = user

    match status_id:
        case 1:
            data["page"]["title"] = "New Orders"
            status = status_id
            items = Order.read_by_joined_status(1, db)
        case 2:
            data["page"]["title"] = "Cooking Orders"
            status = status_id
            items = Order.read_by_joined_status(2, db)
        case 3:
            data["page"]["title"] = "Served orders"
            status = status_id
            items = Order.read_by_joined_status(3, db)
        case 4:
            data["page"]["title"] = "Delete Orders"
            status = status_id
            items = Order.read_by_joined_status(4, db)
        case 5:
            data["page"]["title"] = "Paid Orders"
            status = status_id
            items = Order.read_by_joined_status(5, db)
        case _:
            return "<h1>Wrong Status code</h1>"
    # static section
    context = {
        'data': data,
        'items': items,
        'status': status
    }
    return render_template("cashier/Cashier_order_status.html", **context)


def cashier_table():
    user = get_current_user()
    # route protecting
    if not user:
        return redirect(url_for("login"))
    tables = db.read_all(Table)  # fetch all of tables from database

    # turn status of boolean to string
    for table in tables:
        table.status = "Busy" if table.status else "Free"

    data = {
        "user": user,
        "page": {
            "title": "tables",
        },
        "content": {
            "tables": tables,
        },
    }

    # handle AJAX POST request for changing state of tables
    if request.method == "POST":
        received_data = request.get_json()
        id = received_data["id"]

        if received_data["get_info"]:  # Handle show info section
            orders = Table.current_orders(db, id)
            return render_template("cashier/table_items.html", data=data, orders=orders)
        else:
            table = db.read(Table, id)
            table.status = False
            db.update(table)
            return "200"
    # handle get request
    return render_template("cashier/tables.html", data=data)


def login():
    """login view"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email, password)
        user_info: Cashier = db.read_by(Cashier, ("email", email))

        # user does not exist
        if not user_info or user_info[0].password != password:
            flash("wrong email or password !", "warning")
            return render_template("cashier/login.html")

        # user exists
        res = make_response(redirect(url_for("cashier_dashboard")))
        res.set_cookie("user", email)
        return res

    # Handle get request
    return render_template("cashier/login.html")


def logout():
    """log out"""
    resp = make_response(redirect(url_for("login")))
    resp.delete_cookie("user")
    return resp


@login_required
def cashier_list_menu(user):
    data = {
        "user": user,
    }
    menuitems = db.read_all(MenuItems)
    discounts = db.read_all(Discount)
    categories = db.read_all(Category)
    context = {
        'data': data,
    }
    if request.method == "GET":
        context['menuitems'] = menuitems
        return render_template("cashier/cashier_list_menu.html", **context)

    if request.method == "POST":
        data = request.get_json()

        # get menu item by id
        if data["view"] == "get_item":
            item = db.read(MenuItems, data["items"])
            context.update({
                'item': item,
                'categories': categories,
                'discounts': discounts

            })
            return render_template("cashier/item-modify.html", **context)

        # edit menu item
        elif data["view"] == "edit_item":
            del data['view']
            print(data)
            id = data["id"]
            name = data["name"]
            price = data["price"]
            serving_time = data["serving_time"]
            estimated = data["estimated"]

            try:
                # get discount value
                discount_id = int(data["discount"])
                discount_id = list(filter(lambda d: d.id == int(discount_id), discounts))[0].id
                category_id = data["category"]
                category_id = list(filter(lambda c: c.id == int(category_id), categories))[0].id
            except:
                return Response("{'msg':'something went wrong'}", status=400, mimetype='application/json')

            item_update = db.read(MenuItems, id)
            item_update.name = name
            item_update.price = int(price)
            item_update.serving_time_period = serving_time
            item_update.estimated_cooking_time = int(estimated)
            item_update.picture_link = int(estimated)
            item_update.discount_id = int(discount_id)
            item_update.category_id = int(category_id)
            db.update(item_update)
            context['menuitems'] = menuitems
            return render_template("cashier/cashier_list_menu.html", **context)

        # delete menu item
        elif data["view"] == "del":
            id = data["id"]
            item = db.read(MenuItems, id)
            db.delete(item)
            return "200"
