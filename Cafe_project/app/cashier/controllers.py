from flask import url_for, request, redirect, render_template, \
    make_response, flash, Response, Request, current_app as app, session, jsonify
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from app.models import *
from datetime import datetime
from app.utils.utils import allowed_file
from sqlalchemy.sql import func
from app.extensions import db
from .forms import AddNewTableForm, AboutSettingForm, LoginForm, CashierProfile
from .models import AboutSetting

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename


def get_current_user() -> Cashier:
    """
    return current Cashier object from data if exist in cookies
    """
    user = None

    if "user_email" in session:
        user_email = session.get('user_email')
        user = Cashier.query.filter_by(email=user_email).first()

    return user


def login_required(view):
    """
        takes a view function and check if user is in cookies
    """

    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(url_for(".login"))
        return view(user, *args, **kwargs)

    return wrapper


def login():
    """login view"""
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            cashier = Cashier.query.filter_by(email=form.email.data).first()
            session['user_email'] = cashier.email  # set user email in session
            return redirect(url_for('cashier.cashier_dashboard'))

        # flash form error messages
        if form.errors['email']:
            flash(form.errors['email'][0])
    # Handle get request
    context = {
        'page_title': 'Login'
    }
    return render_template("cashier/login/login.html", form=form, **context)


@login_required
def logout(user):
    """log out"""
    print(user)
    session.pop('user_email', None)
    return redirect(url_for(".login"))


@login_required
def cashier_dashboard(user):
    today_receipts = Receipt.today_receipts()
    report = Receipt.last_week_report()
    form = CashierProfile(obj=user)
    data = {
        "page_title": "Dashboard",
        "user": user,
        "today_earnings": Receipt.calculate_earnings_of_day(),
        "customer_count": len(today_receipts),
    }

    if request.method == "POST":
        if form.validate_on_submit():
            form = CashierProfile(request.form, obj=user)
            form.populate_obj(user)     # update cashier info by form data
            user.set_password(form.password.data)   # hash password
            db.session.commit()
        else:
            err = "\n".join(form.form_errors) if form.form_errors else "Invalid Submission!"
            flash(err, category='error')

        return redirect(url_for('.cashier_dashboard'))


    elif request.method == "GET":
        # send chart info to frontend
        if request.args.get('getChartInfo'):

            chart = {
                "labels": list(map(lambda i: i[1], report)),
                "sum_receipts": list(map(lambda i: i[0], report)),
            }
            return jsonify(chart)

        return render_template("cashier/dashboard/dashboard.html", data=data, form=form)


@login_required
def cashier_order(user):
    if request.method == "GET":
        receipts = Receipt.query.all()

        context = {
            "data": {
                "user": user
            },
            "receipts": receipts
        }

        return render_template("cashier/orders/order-index.html", **context)

    if request.method == "POST":
        # get json payload of request
        request_data = request.get_json()

        context = {
            "status": Status.query.all(),
        }

        # get receipt orders
        if request_data["view"] == "receipt_req":
            context['orders'] = Order.query.filter_by(receipt_id=request_data["receipt_id"]).all()
            return render_template("cashier/orders/receipt-modify.html", **context)

        # change order status of a receipt
        elif request_data["view"] == "status_req":
            receipt_id = request_data["order"]
            status_id = request_data["status_id"]

            Order.query.filter_by(receipt_id=receipt_id).update({
                'status_code_id': int(status_id)
            })
            db.session.commit()
            return render_template(
                "cashier/orders/receipt-modify.html",
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
            items = Order.query.filter_by(status_code_id=1).all()
        case 2:
            data["page"]["title"] = "Cooking Orders"
            status = status_id
            items = Order.query.filter_by(status_code_id=2).all()
        case 3:
            data["page"]["title"] = "Served orders"
            status = status_id
            items = Order.query.filter_by(status_code_id=3).all()
        case 4:
            data["page"]["title"] = "Delete Orders"
            status = status_id
            items = Order.query.filter_by(status_code_id=4).all()
        case 5:
            data["page"]["title"] = "Paid Orders"
            status = status_id
            items = Order.query.filter_by(status_code_id=5).all()
        case _:
            return "<h1>Wrong Status code</h1>"
    # static section
    context = {
        'data': data,
        'items': items,
        'status': status
    }
    return render_template("cashier/orders/Cashier_order_status.html", **context)


# TODO: ADD flask-wtf here
@login_required
def cashier_add_item(user):
    data = {
        "user": user,
    }
    discount = Discount.query.all()
    category = Category.query.all()

    if request.method == "POST":

        try:
            filename = save_and_validate_file(request, 'file')
        except Exception as e:
            flash(str(e))
            return redirect(request.url)
        data = request.form

        image_url = filename
        name = data["name"]
        price = data["price"]
        serving_time_period = data["serving"]
        estimated_cooking_time = data["estimated"]
        discount_id = data.get('discount') or None
        category_id = request.form["category"]

        new_item = MenuItem(
            name=name,
            price=price,
            category_id=category_id,
            serving_time_period=serving_time_period,
            estimated_cooking_time=estimated_cooking_time,
            picture_link=image_url,
            discount_id=discount_id,
        )

        new_item.create()
        flash("Menu Item successfully Added !")
        return redirect(request.url)

    elif request.method == "GET":
        return render_template(
            "cashier/menuitems/cashier_add_item.html",
            discounts=discount,
            categorys=category,
            data=data,
        )


@login_required
def cashier_list_menu(user):
    data = {
        "user": user,
    }
    menuitems = MenuItem.query.all()
    discounts = Discount.query.all()
    categories = Category.query.all()
    context = {
        'data': data,
    }
    if request.method == "GET":
        # get menu item by id
        if menu_item_id := request.args.get('menuItemId'):
            item = MenuItem.query.get(int(menu_item_id))
            context.update({
                'item': item,
                'categories': categories,
                'discounts': discounts

            })
            return render_template("cashier/menuitems/menu_item_modify_modal.html", **context)

        context['menuitems'] = menuitems
        return render_template("cashier/menuitems/cashier_list_menu.html", **context)

    if request.method == "POST":
        data = request.get_json()

        if request.files.get('file'):
            try:
                filename = save_and_validate_file(request, 'file')
            except Exception as e:
                print(e)
                return Response("{'msg':'something went wrong'}", status=400)

            return Response(filename, status=200)

        # edit menu item
        elif data["view"] == "edit_item":
            del data['view']
            print(data)
            data = {**data}

            modified_item = MenuItem.query.get(int(data['id']))
            modified_item.name = data['name']
            modified_item.price = int(data['price'])
            modified_item.serving_time_period = data['serving_time']
            modified_item.estimated_cooking_time = int(data['estimated'])
            modified_item.picture_link = data['image']
            modified_item.discount_id = int(data['discount'])
            modified_item.category_id = int(data['category'])
            db.session.commit()

            return Response("updated", status=200)

    if request.method == "DELETE":
        id = request.args.get('menuItemId')
        menu_item = MenuItem.query.get_or_404(int(id), description='Menu item Not Found!')
        menu_item.delete()
        return "200"


# TODO: ADD flask-wtf here
@login_required
def cashier_add_category(user):
    data = {
        "user": user,
    }
    items_category = Category.query.all()
    items_discount = Discount.query.all()

    context = {
        'items_category': items_category,
        'items_discount': items_discount,
        'data': data,
    }
    if request.method == "GET":
        return render_template("cashier/categories/cashier_add_category.html", **context)

    elif request.method == "POST":

        category_name = request.form.get("category")
        root_id = request.form.get("root_id")
        discount_id = int(request.form.get("discount_id")) or None

        new_category = Category(category_name=category_name, category_root=root_id, discount_id=discount_id)
        new_category.create()

        context = {
            'items_category': items_category,
            'items_discount': items_discount,
            'data': data,
        }
        flash("New Category Added !")
        return render_template("cashier/categories/cashier_add_category.html", **context)


@login_required
def cashier_add_table(user):
    data = {
        "user": user,
        "page": {
            "title": "Add New Table",
        },

    }
    form = AddNewTableForm()
    if request.method == "GET":

        return render_template("cashier/tables/add-table.html", data=data, form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            new_table = Table()
            new_table.position = form.position.data.capitalize()
            new_table.capacity = form.capacity.data
            new_table.create()
            flash('Table Added', 'info')
            return redirect(url_for('.cashier_add_table'))


@login_required
def cashier_table(user):
    tables = Table.query.all()  # fetch all of tables from db

    data = {
        "user": user,
        "page": {
            "title": "tables",
        },
        "content": {
            "tables": tables,
        },
    }
    if request.method == "GET":
        # handle get request
        return render_template("cashier/tables/tables.html", data=data)

    # handle AJAX POST request for changing state of tables
    if request.method == "POST":
        received_data = request.get_json()
        id = received_data["id"]

        if received_data["get_info"]:  # Handle show info section
            orders = Table.current_orders(id)
            return render_template("cashier/tables/table_items.html", data=data, orders=orders)
        else:
            table = Table.query.get(id)
            table.status = False
            db.session.commit()
            return "200"


# TODO: ADD flask-wtf here
@login_required
def cashier_new_discount(user):
    data = {
        "user": user,
    }

    if request.method == "GET":
        return render_template("cashier/discounts/cashier_add_discount.html", data=data)

    elif request.method == "POST":
        discount_value = request.form["persentDiscount"]
        new_discount = Discount(value=int(discount_value))
        try:
            new_discount.create()
            msg = "Discount Successfully Added!"
            status = "success"
        except Exception as e:
            print(e)
            msg = "The entered value is Duplicated!"
            status = "danger"

        flash(msg, status)
        return redirect(request.url)


@login_required
def about_setting(user):
    about_setting = AboutSetting.query.get(1)
    form = AboutSettingForm(obj=about_setting)
    data = {
        "user": user,
        'about_setting': about_setting,
        'page_title': 'About Page Setting'
    }
    if request.method == "GET":
        return render_template("cashier/site_setting/about_setting.html", data=data, form=form)
    if request.method == "POST":
        # data = request.form
        if form.validate_on_submit():
            if not about_setting:
                about_setting = AboutSetting()

            about_setting.paragraph1 = form.paragraph1.data
            about_setting.paragraph2 = form.paragraph2.data
            about_setting.paragraph3 = form.paragraph3.data
            about_setting.banner_url = form.banner_url.data
            about_setting.manager1 = form.manager1.data
            about_setting.manager2 = form.manager2.data
            about_setting.manager3 = form.manager3.data
            about_setting.manager4 = form.manager4.data
            db.session.add(about_setting)
            db.session.commit()

        return redirect(request.url)
