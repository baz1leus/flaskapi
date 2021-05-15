from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.items import ItemResource, ItemListResource
from resources.users import UserRegisterResource
from db import db


def create_app():
    import create_tables

    app = Flask(__name__)
    api = Api(app)

    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    db.init_app(app)

    jwt = JWT(app, authenticate, identity)

    api.add_resource(ItemListResource, '/items')
    api.add_resource(ItemResource, '/items/<string:name>')
    api.add_resource(UserRegisterResource, '/register')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5000', debug=True)
