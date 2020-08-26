import sqlite3

# connect to database
conn = sqlite3.connect("userdata.db")

# create a cursor
c = conn.cursor()

# create a table
c.execute(
    """ CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(30),
    password VARCHAR(100),
    register_date TIMESTAMP DEFAULT CURENT_TIMESTAMP
)
"""
)

# commit changes
conn.commit()

# allways close connection
conn.close()
