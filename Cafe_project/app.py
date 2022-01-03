from flask import Flask
from views import *

app = Flask(__name__)

<<<<<<< HEAD
app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/menu', 'menu', menu, methods=['GET'])
app.add_url_rule('/order/<table_id>', 'order', order, methods=['GET', 'POST', 'DELETE'])
=======
>>>>>>> feature_safa

if __name__ == '__main__':
    app.run()
