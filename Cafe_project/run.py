from app import create_app
import os
from app.cli import register

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'config.{env.capitalize()}Config')

register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)