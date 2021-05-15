from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.users import UserModel

class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')

    def post(self):
        user = UserRegisterResource.parser.parse_args()
        if UserModel.find_by_username(user.username):
            return {'message': 'user already exists'}, 409
        user = UserModel(**user)
        user.add_user()
        return {'message': 'user added'}, 201
