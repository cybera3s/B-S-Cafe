from flask import Flask
from views import *

app = Flask(__name__)

app.add_url_rule('/', 'home', index, methods=['GET'])
app.add_url_rule('/menu', 'menu', menu, methods=['GET'])
app.add_url_rule('/about_us', 'about_us', menu, methods=['GET'])
app.add_url_rule('/contact_us', 'contact_us', menu, methods=['GET', 'POST'])
app.add_url_rule('/order/<table_id>', 'order', order, methods=['GET', 'POST', 'DELETE'])


if __name__ == '__main__':
    app.run()
