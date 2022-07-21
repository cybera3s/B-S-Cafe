from flask import Blueprint

from .controllers import *

landing = Blueprint('landing', __name__, template_folder='templates',
                    static_folder='static/landing', static_url_path='/static/landing')

landing.add_url_rule("/", "index", index, methods=["GET"])
landing.add_url_rule("/home", "home", home, methods=["GET"])
landing.add_url_rule("/menu", "menu", menu, methods=["GET"])
landing.add_url_rule("/about_us", "about_us", about_us, methods=["GET"])
landing.add_url_rule("/contact_us", "contact_us", contact_us, methods=["GET", "POST"])
landing.add_url_rule("/order/<int:table_id>", "order", order, methods=["GET", "POST", "DELETE"])
landing.add_url_rule("/cart", "cart", cart, methods=["GET", "POST", "DELETE"])
landing.add_url_rule('/tables', 'tables', available_tables, methods=["GET"])