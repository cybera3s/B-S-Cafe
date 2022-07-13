from flask import Flask
from flask_cors import CORS

from landing.views import *
from os import urandom
from cashier.views import *
from core.template_filters import format_datetime


app = Flask(__name__, template_folder="templates")
# app configuration
app.config['UPLOAD_FOLDER'] = "static/images/menu_items"
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000  # set maximum volume to 5 MB for a uploaded content

app.secret_key = urandom(24)
CORS(app, origins=["http://localhost*", "http://127.0.0.1"], expose_headers=['receipt_id'])

# template filters
app.add_template_filter(format_datetime, "format_date")

#  -----------  Landing Pages----------------------
app.add_url_rule("/", "index", index, methods=["GET"])
app.add_url_rule("/home", "home", home, methods=["GET"])
app.add_url_rule("/menu", "menu", menu, methods=["GET"])
app.add_url_rule("/about_us", "about_us", about_us, methods=["GET"])
app.add_url_rule("/contact_us", "contact_us", contact_us, methods=["GET", "POST"])
app.add_url_rule("/order/<table_id>", "order", order, methods=["GET", "POST", "DELETE"])
app.add_url_rule("/cart", "cart", cart, methods=["GET", "POST", "DELETE"])

# #  -----------  Cashier Panel---------------------- #

app.add_url_rule("/admin", "login", login, methods=["GET", "POST"])
app.add_url_rule(
    "/cashier_panel/dashboard", "cashier_dashboard", cashier_dashboard, methods=["GET", "POST"]
)
app.add_url_rule(
    "/cashier_panel/order", "cashier_order", cashier_order, methods=["GET", "POST"]
)

app.add_url_rule(
    "/cashier_panel/order/status/<int:status_id>",
    "cashier_order_status",
    cashier_order_status,
    methods=["GET"],
)

app.add_url_rule(
    "/cashier_panel/new_menu_item",
    "cashier_add_item",
    cashier_add_item,
    methods=["POST", "GET"],
)
app.add_url_rule(
    "/cashier_panel/list_menu",
    "cashier_list_menu",
    cashier_list_menu,
    methods=["POST", "GET"],
)
app.add_url_rule(
    "/cashier_panel/add_category",
    "cashier_add_category",
    cashier_add_category,
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/cashier_panel/discount/new_discount",
    "cashier_add_discount",
    cashier_new_discount,
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/cashier_panel/tables", "cashier_table", cashier_table, methods=["GET", "POST"]
)
app.add_url_rule("/cashier_panel/logout", "logout", logout, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)
