# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS

from .core.template_filters import format_datetime
from app.database import db
from app.landing.routes import landing
from app.cashier.routes import cashier


# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
# Import a module / component using its blueprint handler variable (mod_auth)

# 404 HTTP error handling
def page_not_found(error):
    return render_template('404.html'), 404


def create_app(object_name="config.DevConfig"):
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)

    # template filters
    app.add_template_filter(format_datetime, "format_date")

    # Configurations
    CORS(app, origins=["http://localhost*", "http://127.0.0.1"], expose_headers=['receipt_id'])

    app.register_error_handler(404, page_not_found)
    # Register blueprint(s)
    app.register_blueprint(landing)
    app.register_blueprint(cashier)

    return app
