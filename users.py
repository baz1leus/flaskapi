import sqlite3
from flask_restful import reqparse, Resource, abort

parser = reqparse.RequestParser()
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
        
    def __str__(self):
        return 'User(id="%s")' % self.id
    
    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        
        query = 'SELECT * FROM users WHERE username=?'
        row = cur.execute(query, (username,)).fetchone()
        
        con.close()
        
        user = User(*row) if row else None
        return user
    
    
    @staticmethod
    def find_by_id(_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        
        query = 'SELECT * FROM users WHERE id=?'
        row = cur.execute(query, (_id,)).fetchone()
        
        con.close()
        
        user = User(*row) if row else None
        return user

class UserRegister(Resource):
    def post(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        print(list(cur.execute(f'SELECT * FROM users WHERE username = "{args["username"]}"')))
        if cur.execute(f'SELECT * FROM users WHERE username = "{args["username"]}"').fetchone():
            abort(409, message="User Already Exists")
        else:
            user = (args['username'], args['password'])
            cur.execute('INSERT INTO users(id, username, password) VALUES (NULL, ?, ?)', user)
            con.commit()
            con.close()
            return {'message': f'added {args["username"]}'}, 201
