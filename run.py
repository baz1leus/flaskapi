from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

items = [
    {
        'name': 'chairs',
        'price': 1500,
    },
    {
        'name': 'chair-2',
        'price': 999,
    },
    {
        'name': 'chair-3',
        'price': 1999,
    },
]

parser = reqparse.RequestParser()


class Item(Resource):
    # GET /items/<name>
    def get(self, name):
        _item = list(filter(lambda x: x['name'] == name, items))
        if _item:
            return {'searched_item': _item[0]}
        return {'message': 'not found'}
    
    # POST /items/<name>
    def post(self, name):
        parser.add_argument('price')
        _item = list(filter(lambda x: x['name'] == name, items))
        if _item:
            return {'message': 'item already exists'}
        if parser.parse_args()['price'].isdigit():
            items.append({'name': name, 'price': int(parser.parse_args()['price'])})
            return {'items': items}
        else:
            return {'message': 'price should be an integer'}
    
    # PUT /items/<name>
    def put(self, name):
        parser.add_argument('price')
        _item = list(filter(lambda x: x['name'] == name, items))
        if _item:
            if parser.parse_args()['price'].isdigit():
                _item[0]['price'] = int(parser.parse_args()['price'])
                return {'items': items}
            else:
                return {'message': 'price should be an integer'}
        if parser.parse_args()['price'].isdigit():
            items.append({'name': name, 'price': int(parser.parse_args()['price'])})
            return {'items': items}
        else:
            return {'message': 'price should be an integer'}
    
    # DELETE /items/<name>
    def delete(self, name):
        _item = list(filter(lambda x: x['name'] == name, items))
        if _item:
            items.remove(_item[0])
            return {'items': items}
        return {'message': 'not found'}


api.add_resource(Item, '/items/<name>')


class ItemList(Resource):
    
    # GET /items
    def get(self):
        return {'items': items}
    
    
    # POST /items
    def post(self):
        parser.add_argument('itemlist', type=dict, action='append')
        _itemlist = parser.parse_args()['itemlist']
        
        errors = []
        for item in _itemlist:
            _item = list(filter(lambda x: x['name'] == item['name'], items))
            if _item:
                errors.append(item['name']+' already exists')
            else:
                if isinstance(item['price'], int):
                    items.append({'name': item['name'], 'price': item['price']})
                else:
                    errors.append(item['name']+' price should be an integer')
        return {'errors': errors, 'items': items}

api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)
