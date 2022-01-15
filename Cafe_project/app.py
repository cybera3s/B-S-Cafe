from flask import Flask
from views.landing_views import *
from views import cashier_add_category, cashier_add_discount, cashier_add_item, cashier_dashboard, cashier_order, \
    cashier_table, login
from os import urandom
from views import cashier_status_orders

app = Flask(__name__, template_folder='templates')
app.secret_key = urandom(24)


#  -----------  Landing Pages----------------------

app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/home', 'home', home, methods=['GET'])
app.add_url_rule('/menu', 'menu', menu, methods=['GET'])
app.add_url_rule('/about_us', 'about_us', about_us, methods=['GET'])
app.add_url_rule('/contact_us', 'contact_us', contact_us, methods=['GET', 'POST'])
app.add_url_rule('/order/<table_id>', 'order', order, methods=['GET', 'POST', 'DELETE'])
app.add_url_rule('/cart', 'cart', cart, methods=['GET', 'POST', 'DELETE'])

# #  -----------  Cashier Panel---------------------- #

app.add_url_rule('/cashier_panel', 'login',login.login, methods=['GET', 'POST']) # --------> (safa)
app.add_url_rule('/cashier_panel/dashboard', 'cashier_dashboard', cashier_dashboard.cashier_dashboard, methods=['GET']) # --------> (safa)
app.add_url_rule('/cashier_panel/order', 'cashier_order', cashier_order.cashier_order, methods=['GET', 'POST'])  # --------> () (mamreza)
app.add_url_rule('/cashier_panel/order/served', 'cashier_order_served', cashier_status_orders.cashier_order_served, methods=['GET'])# --------> (mamad nasimi)
app.add_url_rule('/cashier_panel/order/paid', 'cashier_paid_order', cashier_status_orders.cashier_paid_order,  methods=['GET']) #--------> (mamad nasimi)
app.add_url_rule('/cashier_panel/order/delete', 'cashier_delete_order', cashier_status_orders.cashier_delete_order,  methods=['GET']) #--------> (mamad nasimi)
app.add_url_rule('/cashier_panel/order/cook', 'cashier_cook_order', cashier_status_orders.cashier_cook_order,  methods=['GET']) #--------> (mamad nasimi)
app.add_url_rule('/cashier_panel/new_menu_item', 'cashier_add_item', cashier_add_item.cashier_add_item, methods=['POST', 'GET']) #--------> (mamreza)
app.add_url_rule('/cashier_panel/add_category', 'cashier_add_category', cashier_add_category.cashier_add_category, methods=['GET', 'POST']) #--------> (mamad nasimi)


if __name__ == '__main__':
    app.run(debug=True)
