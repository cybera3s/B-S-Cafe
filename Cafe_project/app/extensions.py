from flask_migrate import Migrate
from flask_mail import Mail


mail = Mail()
migrate = Migrate()
@celery.task()
def test():
    return 'ok'