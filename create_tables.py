import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)')
cur.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price integer)')

con.commit()
con.close()
