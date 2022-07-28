from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
