from flask import Flask
from landing.landing_views import *
from os import urandom
from cashier.views import *

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

app.add_url_rule('/cashier_panel', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/cashier_panel/dashboard', 'cashier_dashboard', cashier_dashboard, methods=['GET'])
app.add_url_rule('/cashier_panel/order', 'cashier_order', cashier_order, methods=['GET', 'POST'])
app.add_url_rule('/cashier_panel/order/served', 'cashier_order_served', cashier_order_served, methods=['GET'])
app.add_url_rule('/cashier_panel/order/paid', 'cashier_paid_order', cashier_paid_order, methods=['GET'])
app.add_url_rule('/cashier_panel/order/delete', 'cashier_delete_order', cashier_delete_order, methods=['GET'])
app.add_url_rule('/cashier_panel/order/cook', 'cashier_cook_order', cashier_cook_order, methods=['GET'])
app.add_url_rule('/cashier_panel/new_menu_item', 'cashier_add_item', cashier_add_item, methods=['POST', 'GET'])
app.add_url_rule('/cashier_panel/list_menu', 'cashier_list_menu', cashier_list_menu, methods=['POST', 'GET'])
app.add_url_rule('/cashier_panel/add_category', 'cashier_add_category', cashier_add_category, methods=['GET', 'POST'])
app.add_url_rule('/cashier_panel/order/new-order', 'cashier_order_new', cashier_new_order, methods=['GET'])
app.add_url_rule('/cashier_panel/discount/new_discount', 'cashier_add_discount', cashier_new_discount,
                 methods=['GET', 'POST'])
app.add_url_rule('/cashier_panel/tables', 'cashier_table', cashier_table, methods=['GET', 'POST'])
app.add_url_rule('/cashier_panel/logout', 'logout', logout, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
