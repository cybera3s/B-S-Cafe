from flask import Flask
from views.landing_views import *
from views import cashier_add_category, cashier_add_discount, cashier_add_item, cashier_dashboard, cashier_order, \
    cashier_order_served, cashier_table, login

app = Flask(__name__, template_folder='templates')

#  -----------  Landing Pages----------------------

app.add_url_rule('/', 'home', index, methods=['GET'])
app.add_url_rule('/menu', 'menu', menu, methods=['GET'])
app.add_url_rule('/about_us', 'about_us', about_us, methods=['GET'])
app.add_url_rule('/contact_us', 'contact_us', contact_us, methods=['GET', 'POST'])
app.add_url_rule('/order/<table_id>', 'order', order, methods=['GET', 'POST', 'DELETE'])

# #  -----------  Cashier Panel ---------------------- #

# # app.add_url_rule('/cashier_panel', 'login',login.login, methods=['GET', 'POST']) # --------> (safa)
# # app.add_url_rule('/cashier_panel/dashboard', 'cashier_dashboard', cashier_dashboard.cashier_dashboard, methods=['GET']) # --------> (safa)
# # app.add_url_rule('/cashier_panel/table', 'cashier_table', cashier_table.cashier_table, methods=['GET']) # --------> (amirali)
# # app.add_url_rule('/cashier_panel/order', 'cashier_order', cashier_order.cashier_order, methods=['GET']) # --------> () (mamreza)
# # app.add_url_rule('/cashier_panel/order/served', 'cashier_order_served', cashier_order_served.cashier_order_served, methods=['GET']) --------> (mamad nasimi)
# # app.add_url_rule('/cashier_panel/new_menu_item', 'cashier_add_item', cashier_add_item.cashier_add_item, methods=['POST']) --------> (mamreza)
# # app.add_url_rule('/cashier_panel/add_category', 'cashier_add_category', cashier_add_category.cashier_add_category, methods=['GET', 'POST']) --------> (mamad nasimi)
# # app.add_url_rule('/cashier_panel/add_discount', 'cashier_add_discount', cashier_add_discount.cashier_add_discount, methods=['GET', 'POST']) --------> (meisam)

# # for now optional
# # app.add_url_rule('/cashier_panel/edit_menu', cashier_edit_menu.cashier_edit_menu, methods=['GET', 'POST']) --------> (safa and alireza)


if __name__ == '__main__':
    app.run(debug=True)
