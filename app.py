from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from items import Item, ItemList
from create_tables import create_tables
from users import UserRegister

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'


create_tables()

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(debug=True)
