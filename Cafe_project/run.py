import sys
import os

from app import create_app
from app.cli import register
from app.utils.utils import check_email_configuration

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'config.{env.capitalize()}Config')

# check email and celery configuration
try:
    check_email_configuration(app)
except Exception as e:
    print(str(e))
    sys.exit()

register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
