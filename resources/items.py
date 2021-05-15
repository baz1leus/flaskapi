from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.items import ItemModel

class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=int)

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item(name)
        if not item:
            return {'message': 'item doesn\'t exist'}, 404
        return {'name': item.name, 'price': item.price}, 200

    @jwt_required()
    def post(self, name):
        if ItemModel.get_item(name):
            return {'message': 'item already exists'}, 400
        price = ItemResource.parser.parse_args()['price']
        item = ItemModel(name=name, price=price)
        item.add_item()
        return {'name': name, 'price': price}, 201

    @jwt_required()
    def put(self, name):
        price = ItemResource.parser.parse_args()['price']
        if not ItemModel.get_item(name):
            item = ItemModel(name=name, price=price)
            item.add_item()
            return {'name': name, 'price': price}, 201
        ItemModel.update_item(name, price)
        return {'name': name, 'price': price}, 200

    @jwt_required()
    def delete(self, name):
        item = ItemModel.get_item(name)
        if not item:
            return {'message': 'item doesn\'t exist'}, 404
        item.delete_item()
        return {}, 204


class ItemListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, action='append')
    
    @jwt_required()
    def get(self):
        items = ItemModel.get_items()
        return {'items': [{'name': item.name, 'price': item.price} for item in items]}

    @jwt_required()
    def post(self):
        items = ItemListResource.parser.parse_args()['items']
        errors = []
        for item in items:
            if ItemModel.get_item(item['name']):
                errors.append(item['name'])
        if errors:
            return {'message': f'{errors} already exist'}, 400
        
        for item in items:
            new_item = ItemModel(name=item['name'], price=item['price'])
            new_item.add_item()
        return {'items': items}, 201

