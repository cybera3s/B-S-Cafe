from flask import Blueprint

from .controllers import *

cashier = Blueprint('cashier', __name__, template_folder='templates',
                    static_folder='static', url_prefix="/admin", static_url_path='assets')

cashier.add_url_rule("/login", "login", login, methods=["GET", "POST"])
cashier.add_url_rule(
    "/cashier_panel/dashboard", "cashier_dashboard", cashier_dashboard, methods=["GET", "POST"]
)
cashier.add_url_rule(
    "/cashier_panel/order", "cashier_order", cashier_order, methods=["GET", "POST", "PUT"]
)

cashier.add_url_rule(
    "/cashier_panel/order/status/<int:status_id>",
    "cashier_order_status",
    cashier_order_status,
    methods=["GET", "POST"],
)

cashier.add_url_rule(
    "/cashier_panel/new_menu_item",
    "cashier_add_item",
    cashier_add_item,
    methods=["POST", "GET"],
)
cashier.add_url_rule(
    "/cashier_panel/list_menu",
    "cashier_list_menu",
    cashier_list_menu,
    methods=["POST", "GET", 'DELETE'],
)
cashier.add_url_rule(
    "/cashier_panel/add_category",
    "cashier_add_category",
    cashier_add_category,
    methods=["GET", "POST"],
)
cashier.add_url_rule(
    "/cashier_panel/discount/new_discount",
    "cashier_add_discount",
    cashier_new_discount,
    methods=["GET", "POST"],
)
cashier.add_url_rule(
    "/cashier_panel/tables", "cashier_table", cashier_table, methods=["GET", "POST"]
)

cashier.add_url_rule(
    "/cashier_panel/tables/add", "cashier_add_table", cashier_add_table, methods=["GET", "POST"]
)
cashier.add_url_rule("/cashier_panel/logout", "logout", logout, methods=["GET", "POST"])
cashier.add_url_rule('/cashier_panel/site-setting/about', "about_setting", about_setting, methods=["GET", "POST"])