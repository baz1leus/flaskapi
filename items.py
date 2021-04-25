from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt import jwt_required
import sqlite3


parser = reqparse.RequestParser()
parser.add_argument('price', type=int)
parser.add_argument('itemlist', type=dict, action="append")


class Item(Resource):
    # GET /items/<name>
    @jwt_required()
    def get(self, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        row = cur.execute('SELECT * FROM items WHERE name=?', (name,)).fetchone()
        con.close()
        
        item = [*row] if row else None
        if item:
            return {'item': item}
        
        abort(404, message="Item Not Found")
    
    
    # POST /items/<name>
    @jwt_required()
    def post(self, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        row = cur.execute('SELECT * FROM items WHERE name=?', (name,)).fetchone()
        
        if row:
            abort(409, message="Item Already Exists")
        
        args = parser.parse_args()
        item = (name, args['price'])
        
        cur.execute('INSERT INTO items VALUES (NULL, ?, ?)', item)
        
        con.commit()
        con.close()
        return {'message': f'added {item}'}, 201
    

    # PUT /items/<name>
    @jwt_required()
    def put(self, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        row = cur.execute('SELECT * FROM items WHERE name=?', (name,)).fetchone()
        
        args = parser.parse_args()
        item = (name, args['price'])

        if row:
            cur.execute(f'UPDATE items SET price = {0} WHERE name = "{1}"'.format(item))
            
            con.commit()
            con.close()

            return {'message': f'updated {item}'}, 200

        cur.execute('INSERT INTO items VALUES (NULL, ?, ?)', item)
        
        con.commit()
        con.close()
        return {'message': f'added {item}'}, 201

    
    # DELETE /items/<name>
    @jwt_required()
    def delete(self, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        row = cur.execute('SELECT * FROM items WHERE name=?', (name,)).fetchone()
        

        item = [*row] if row else None

        if item:
            cur.execute(f'DELETE from items WHERE name = "{name}"')
            con.commit()
            con.close()
            return {'message': f'removed {item}'}
        
        con.close()
        abort(404, message="Item Not Found")


class ItemList(Resource):
    
    # GET /items
    @jwt_required()
    def get(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        
        items = list(cur.execute('SELECT * FROM items'))
        
        con.close()
        return {'items': items}, 200

    
    
    # POST /items
    @jwt_required()
    def post(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        
        args = parser.parse_args()
        
        messages = []
        
        for item in args['itemlist']:
            try:
                _item = (item['name'], int(item['price']))
            except ValueError as e:
                messages.append(str(e))
            
            row = cur.execute('SELECT * FROM items WHERE name=?', (item['name'],)).fetchone()
            
            if row:
                messages.append(f'Item Already Exists {_item}')
            else:
                cur.execute('INSERT INTO items VALUES (NULL, ?, ?)', _item)
                
                messages.append(f'added {_item}')
        
        con.commit()
        con.close()

        return {'message': messages}, 200
