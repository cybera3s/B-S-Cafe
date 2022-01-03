from flask import Flask
from views import *

app = Flask(__name__)

app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/menu', 'menu', menu, methods=['GET'])
app.add_url_rule('/order/<table_id>', 'index', order, methods=['GET', 'POST', 'DELETE'])


if __name__ == '__main__':
    app.run()
