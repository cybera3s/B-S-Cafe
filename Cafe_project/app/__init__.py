
def create_app(object_name="config.DevConfig", register_blueprints=True):
    from flask_cors import CORS
    from flask import Flask, render_template
    # local imports
    from .extensions import mail, migrate
    from .core.template_filters import format_datetime
    from app.extensions import db
    from .models import bcrypt

    # 404 HTTP error handling
    def page_not_found(error):
        return render_template('404.html'), 404

    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)

    # template filters
    app.add_template_filter(format_datetime, "format_date")

    # Configurations
    CORS(app, origins=["http://localhost*", "http://127.0.0.1"])

    app.register_error_handler(404, page_not_found)
    # Register blueprint(s)
    if register_blueprints:
        from app.landing import create_module as landing_create_module
        from app.cashier import create_module as cashier_create_module
        landing_create_module(app)
        cashier_create_module(app)

    return app
