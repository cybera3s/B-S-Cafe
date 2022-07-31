def create_module(app, **kwargs):
    from .routes import cashier
    from app.models import Status

    @cashier.context_processor
    def inject_status():
        return dict(all_status=Status.query.all())

    @cashier.context_processor
    def inject_site_data():
        from datetime import datetime
        return dict(site_name=app.config.get('SITE_NAME'), current_year=datetime.now().year)
    app.register_blueprint(cashier)
