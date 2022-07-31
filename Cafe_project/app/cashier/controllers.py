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
from .forms import AddNewTableForm, AboutSettingForm, LoginForm, CashierProfile, MenuItemForm, AddCategoryForm
from .models import AboutSetting
from sqlalchemy.ext import baked
from sqlalchemy.orm import Session
from flask_wtf.file import FileRequired
from flask.views import MethodView

base_variables = {
    "page": {"lang": "en-US", "title": ""},
}


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
        if form.form_errors:
            errors = "\n".join(form.form_errors)
            flash(errors)
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
            form.populate_obj(user)  # update cashier info by form data
            user.set_password(form.password.data)  # hash password
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
    s = Session(bind=db.engine)  # create db session
    # cache receipt query
    bakery = baked.bakery()
    receipts_query = bakery(lambda s: s.query(Receipt))
    status_query = bakery(lambda s: s.query(Status))

    context = {
        "status": status_query(s).all(),
    }
    if request.method == "GET":
        context.update({
            "data": {
                "user": user
            },
            "receipts": receipts_query(s).all(),
            "page_title": "Orders",
        })
        # get receipt orders by receipt id from query parameters
        if receipt_id := request.args.get('receipt_id'):
            if receipt := receipts_query(s).get(receipt_id):
                context['orders'] = receipt.orders
                return render_template("cashier/orders/receipt-modify.html", **context)
            else:
                return Response('Receipt Not Found', status=404)

        # Handle GET request with no query parameters
        return render_template("cashier/orders/order-index.html", **context)

    elif request.method == "PUT":
        # get json payload of request
        data = request.get_json()
        # change order status of a receipt
        order_id = data["orderId"]
        status_id = data["statusId"]

        # Update order status
        order = Order.query.get(order_id)
        order.status_code_id = int(status_id)
        db.session.commit()

        return render_template(
            "cashier/orders/receipt-modify.html",
            **context
        )


@login_required
def cashier_order_status(user, status_id):
    data = base_variables
    data["user"] = user

    status = Status.query.get_or_404(status_id)
    data["page"]["title"] = status.status.capitalize() + ' Orders'
    orders = status.orders

    # static section
    context = {
        'data': data,
        'orders': orders,
        'status': status,

    }
    # update statuses
    if request.method == "POST":
        if request.form.get('updateTable'):
            return render_template("cashier/orders_status/table_body.html", **context)

    return render_template("cashier/orders_status/cashier_order_status.html", **context)


@login_required
def cashier_add_item(user):
    data = base_variables
    form = MenuItemForm()
    # set discount and category choices => <option value="model_id">model_value</option>
    form.discount.choices += ([(d.id, str(d.value) + '%') for d in Discount.query.all()])
    form.category.choices += ([(c.id, c.category_name) for c in Category.query.all()])

    data |= {"user": user, }

    if request.method == "POST":
        if form.validate_on_submit():
            file = form.image.data
            filename = secure_filename(file.filename)  # remove unsafe characters from image name
            # check if upload folder exists else make it
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder, exist_ok=True)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_item = MenuItem(
                name=form.name.data,
                price=form.price.data,
                category_id=form.category.data,
                serving_time_period=form.serving_time_period.data,
                estimated_cooking_time=form.estimated_cooking_time.data,
                picture_link=filename,
                discount_id=form.discount.data,
            )

            new_item.create()
            flash("Menu Item successfully Added !", category='success')
            return redirect(request.url)
        else:
            flash("Please Correct Below Errors!", "danger")

    return render_template(
        "cashier/menuitems/cashier_add_item.html",
        data=data, form=form
    )


@login_required
def cashier_list_menu(user):
    data = {
        "user": user,
    }
    menuitems = MenuItem.query.all()

    context = {
        'data': data,
        'page_title': 'Menu Items',
    }
    form = MenuItemForm()
    # set discount and category choices => <option value="model_id">model_value</option>
    form.discount.choices += ([(d.id, str(d.value) + '%') for d in Discount.query.all()])
    form.category.choices += ([(c.id, c.category_name) for c in Category.query.all()])

    if request.method == "GET":

        # get menu item by id
        if menu_item_id := request.args.get('menuItemId'):
            item = MenuItem.query.get(int(menu_item_id))
            form = MenuItemForm(obj=item)
            # set discount and category choices => <option value="model_id">model_value</option>
            form.discount.choices += ([(d.id, str(d.value) + '%') for d in Discount.query.all()])
            form.category.choices += ([(c.id, c.category_name) for c in Category.query.all()])
            # set initial category and discount
            form.category.data = item.category_id
            form.discount.data = item.discount_id
            form.image.data = item.picture_link
            context |= {
                'item': item,
                'form': form
            }
            return render_template("cashier/menuitems/menu_item_modify_modal.html", **context)

        context['menuitems'] = menuitems
        return render_template("cashier/menuitems/cashier_list_menu.html", **context)

    if request.method == "POST":
        # remove required validator from image field of form
        if isinstance(form.image.validators[0], FileRequired):
            form.image.validators.pop(0)

        if form.validate_on_submit():
            file = form.image.data
            filename = None

            if file:
                filename = secure_filename(file.filename)  # remove unsafe characters from image name
                # check if upload folder exists else make it
                upload_folder = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder, exist_ok=True)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            menu_item = MenuItem.query.get(form.id.data)

            menu_item.name = form.name.data
            menu_item.price = form.price.data
            menu_item.category_id = form.category.data
            menu_item.serving_time_period = form.serving_time_period.data
            menu_item.estimated_cooking_time = form.estimated_cooking_time.data
            menu_item.picture_link = filename or menu_item.picture_link
            menu_item.discount_id = form.discount.data
            db.session.commit()
            return Response("Updated", status=200)

        else:

            response = make_response(jsonify(form.errors))
            response.status_code = 400
            return response

    if request.method == "DELETE":
        id = request.args.get('menuItemId')
        menu_item = MenuItem.query.get_or_404(int(id), description='Menu item Not Found!')
        menu_item.delete()
        return "200"



class CategoryView(MethodView):
    decorators = [login_required]
    template_name = "cashier/categories/category_index.html"
    data = {
        "page_title": "Category Index",
    }

    def get(self, user):
        categories = Category.query.all()
        self.data |= {
            'categories': categories,
            'user': user
        }
        return render_template(self.template_name, data=self.data)



@login_required
def cashier_add_category(user):
    data = {
        "user": user,
        "page_title": "Add Category"
    }
    form = AddCategoryForm()
    form.discount_id.choices += ([(d.id, str(d.value) + '%') for d in Discount.query.all()])
    form.category_root.choices += ([(c.id, c.category_name) for c in Category.query.all()])

    context = {
        'data': data,
        'form': form
    }
    if request.method == "GET":
        return render_template("cashier/categories/cashier_add_category.html", **context)

    elif request.method == "POST":
        if form.validate_on_submit():
            new_category = Category(
                category_name=form.category_name.data,
                category_root=form.category_root.data,
                discount_id=form.discount_id.data
            )
            new_category.create()

            flash("New Category Added !", category='success')
            return render_template("cashier/categories/cashier_add_category.html", **context)

        flash("Something went wrong", category='danger')
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
            "title": "Tables",
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


@login_required
def cashier_new_discount(user):
    data = {
        "user": user,
        "page_title": "Add New Discount"
    }

    if request.method == "GET":
        return render_template("cashier/discounts/cashier_add_discount.html", data=data)

    elif request.method == "POST":
        discount_value = request.form["discountValue"]
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
