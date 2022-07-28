
def create_module(app, **kwargs):
    from .routes import cashier
    app.register_blueprint(cashier)
