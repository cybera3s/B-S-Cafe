from run import app
from app.extensions import db
from app.models import *
from app import migrate
from app.cashier.models import *


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, cashier=Cashier, table=Table, receipt=Receipt, order=Order, status=Status,
                menuitem=MenuItem, discount=Discount, category=Category, migrate=migrate,
                about_setting=AboutSetting
                )
