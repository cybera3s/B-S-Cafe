import json
from flask import request, render_template, redirect, url_for, \
    Response, jsonify, make_response, Request, abort

from app.cashier.models import AboutSetting
from app.models import *
from .forms import ContactUsForm
from .tasks import send_email

base_variables = {
    "pages": {
        "home": {"title": "Home", "endpoint": "home"},
        "menu": {"title": "Menu", "endpoint": "menu"},
        "about_us": {"title": "About", "endpoint": "about_us"},
        "contact_us": {"title": "Contact Us", "endpoint": "contact_us"},
    },
    "current_page": "",
    "site_name": "Bitter & Sweet"
}


def available_tables():
    """
        return serialized free tables on get request
    """
    tables = Table.query.filter(status, False).all()  # read tables that are empty
    serialized_tables = list(map(lambda t: vars(t), tables))
    return jsonify(serialized_tables)


def index():
    data = base_variables
    data["current_page"] = "index"
    tables = Table.query.filter(Table.status == False).all()  # read tables that are empty
    context = {
        'data': data,
        'tables': tables
    }
    if request.method == "GET":
        data["title"] = "home"
        return render_template("landing/index.html", **context)


def home():
    data = base_variables
    data["current_page"] = "index"
    tables = Table.query.filter(Table.status == False).all()  # read tables that are empty

    context = {
        'data': data,
        'tables': tables
    }
    if request.method == "GET":
        return render_template("landing/home/home.html", **context)


def set_final_price(item: MenuItem):
    """
        get menu item and bind final price to it then return it
    """
    item.final_price = item.final_price()
    return item


def menu():
    """
        show menu items on GET request
    """
    discounts = Discount.query.all()
    data = base_variables
    data["current_page"] = "menu"
    items = MenuItem.query.all()
    modified_items = list(map(set_final_price, items))

    if request.method == "GET":
        data["title"] = "menu"
        context = {
            'items': modified_items,
            'data': data,
            'discounts': discounts
        }
        return render_template("landing/menu.html", **context)


def order(table_id: int):
    """
        select table on GET request
        add to cart on POST request
    """
    table = Table.query.get(table_id)
    if not table:
        return Response("Table Not Found!", status=404)
    # table selecting
    if request.method == "GET":
        return table_select(table_id, table)

    # Add To Cart
    elif request.method == "POST":
        return add_to_cart(request)


def table_select(table_id: int, table: Table) -> Response:
    """
       if table is free and receipt is pending in cookies then returns
       response with table id as cookie
       else if table is full returns 400 response

    """
    # get data from db for response
    data = base_variables
    data["current_page"] = "order"
    items = MenuItem.query.all()
    modified_items = map(set_final_price, items)

    discounts = Discount.query.all()
    context = {
        'data': data,
        'items': modified_items,
        'discounts': discounts
    }
    response = make_response(render_template("landing/order.html", **context))
    # check if table is empty
    if table.status:
        return Response("Table is Busy", status=400)

    cookie_receipt = request.cookies.get('receipt')
    # if receipt is not pending then pend it
    if not cookie_receipt:
        response.set_cookie('receipt', 'pending')

    response.set_cookie('table_id', str(table_id))
    return response


def add_to_cart(request: Request) -> Response:
    """
        Add to cart using cookies
        :param request : a flask request object\n
        :returns a Response object\n
    """
    data = request.get_json()
    if not data:
        return Response("Request Body is not provided", status=400)
    # unpack data from request data payload
    menu_item_id = data.get('itemId')
    item_count = data.get('itemCount')
    item_name = data.get('itemName')
    item_price = data.get('itemPrice')
    item_final_price = data.get('finalPrice')
    # Check Payload data for 0 or None type
    if not all(i for i in [item_count, menu_item_id, item_name, item_price]):
        err_msg = "one of the (menu item id,count,name,price) is not provided!"
        return Response(err_msg, status=400)

    response = make_response({'msg': 'ok'})
    #  get receipt from cookies and check if its pending
    receipt = request.cookies.get('receipt')

    if not receipt:
        return Response("You have no Receipt yet!", status=400)

    cookie_orders = request.cookies.get('orders')
    # check if orders exist in cookies
    if cookie_orders:
        orders = json.loads(cookie_orders)  # 9
        # menu item already exist in cookies orders
        if orders.get(str(menu_item_id)):
            orders[str(menu_item_id)]['count'] += item_count
        else:  # menu item is new in cookies orders
            orders[str(menu_item_id)] = {
                "count": item_count,
                "name": item_name,
                "price": item_price,
                "item_final_price": item_final_price
            }
    # new order
    else:

        orders = {
            menu_item_id: {
                'count': item_count,
                "name": item_name,
                "price": item_price,
                "item_final_price": item_final_price
            }
        }

    dumped_orders = json.dumps(orders)  # serialize orders as json
    response.set_cookie('orders', dumped_orders)
    return response


def cart():
    """
        GET request: get orders from cookies
        POST request: complete payment
    """

    # cookies orders validation
    cookie_orders = request.cookies.get('orders')
    if not cookie_orders:
        return Response("There is no orders", status=400)

    orders = json.loads(cookie_orders)
    if not isinstance(orders, dict) or not orders:
        return Response("Empty or Bad Orders Type", status=400)

    # get orders of cart
    if request.method == "GET":
        # show cart items

        orders = orders.values()

        total_price = 0
        final_price = 0
        # calculate total and final price
        for o in orders:
            total_price += o['count'] * o['price']
            final_price += o['count'] * (o['item_final_price'] or o['price'])

        context = {
            'orders': orders,
            'total_price': total_price,
            'final_price': final_price
        }
        return render_template("landing/cart.html", **context)

    # payment
    elif request.method == "POST":
        data = request.form
        # check request body
        if not data:
            return Response("Request Body is not provided", status=400)

        total_price = data.get('totalPrice')
        final_price = data.get('finalPrice')
        receipt = request.cookies.get('receipt')
        table_id = request.cookies.get('table_id')
        orders = request.cookies.get('orders')

        # convert to numbers
        try:
            final_price = float(final_price)
            total_price = float(total_price)
            if not total_price or not final_price:
                return Response("total price or final price is not provided", status=400)
        except Exception as e:
            print(e)
            # check type of total and final price body args
            return Response("Invalid Type for total price or final price(expected Integer or Float)", status=400)

        # check table id exist in cookies and its type
        if not table_id:
            return Response("Table id is not Provided in cookies", status=400)

        current_table = Table.query.filter((Table.id == table_id) & (Table.status == False)).first()
        if not current_table:
            return Response("Table is not empty, try Another Table", status=400)
        if not receipt or receipt != 'pending':
            return Response("You have no Receipt yet!", status=400)

        orders = json.loads(orders)
        # register Receipt
        receipt = Receipt(table_id=int(table_id))
        receipt.is_paid = True
        receipt.total_price = total_price
        receipt.final_price = final_price
        receipt.create()

        # register order objects
        for item_id, detail in orders.items():
            menu_item = MenuItem.query.get(item_id)
            if not menu_item:
                return Response("Invalid Menu Item!", status=400)

            if not detail['count'] or detail['count'] <= 0:
                return Response("Invalid Count for Item!", status=400)

            order_obj = Order(
                menu_item_id=item_id,
                status_code_id=1,
                count=detail['count'],
                receipt_id=receipt.id
            )
            order_obj.create()

        # update and save table status
        current_table.status = True
        db.session.commit()
        # prepare response and delete old cookies
        response = make_response(redirect(url_for(".home")))
        response.set_cookie('receipt_id', str(receipt.id))
        response.delete_cookie('orders')
        response.delete_cookie('receipt')

        return response


def about_us():
    """
        About Us page
    """
    data = base_variables
    data["current_page"] = "about_us"
    about_setting = AboutSetting.query.get(1)

    if request.method == "GET":
        return render_template("landing/about_us/about_us.html", data=data, about_setting=about_setting)


def contact_us():
    """
        Contact us page
    """
    data = base_variables
    form = ContactUsForm()
    data["current_page"] = "contact_us"
    if request.method == "GET":
        return render_template("landing/contact_us/contact_us.html", data=data, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            data = {
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'email': form.email.data,
                'feedback': form.feedback.data
            }
            try:
                # send email using celery task
                send_email.delay(data)
                return Response("Thanks for your Feedback", status=200)
            except Exception as e:
                print(e)
                return Response("Something Went Wrong on Sending Feedback, Try again later", status=400)

        return Response("Invalid Submission of Form", status=400)
