import sqlite3

def create_tables():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)')
    cur.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price integer)')
    
    con.commit()
    con.close()


'''
create_user = 'INSERT INTO users VALUES (None, ?, ?)'
user = ('bazileus', '1234')
cur.execute(create_user, user)




create_item = 'INSERT INTO items VALUES (None, ?, ?)'
item = ('chair', '1221')
cur.execute(create_item, item)
'''
