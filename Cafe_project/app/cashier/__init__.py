def create_module(app, **kwargs):
    from .routes import cashier
    from app.models import Status

    @cashier.context_processor
    def inject_status():
        return dict(all_status=Status.query.all())

    app.register_blueprint(cashier)
