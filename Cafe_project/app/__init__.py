# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS

from app.database.manager import db
from .core.template_filters import format_datetime


# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
# Import a module / component using its blueprint handler variable (mod_auth)

# Define the WSGI application object
# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)


# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
def create_app(config_filename='config'):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # template filters
    app.add_template_filter(format_datetime, "format_date")

    # Configurations
    CORS(app, origins=["http://localhost*", "http://127.0.0.1"], expose_headers=['receipt_id'])

    # Sample HTTP error handling
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Register blueprint(s)
    from app.landing.routes import landing
    from app.cashier.routes import cashier
    app.register_blueprint(landing)
    app.register_blueprint(cashier)

    return app
