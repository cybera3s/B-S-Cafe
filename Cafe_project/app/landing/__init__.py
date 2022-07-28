
def create_module(app, **kwargs):
    from .routes import landing
    app.register_blueprint(landing)
