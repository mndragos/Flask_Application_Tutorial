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
    register_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
)
"""
)

# commit changes
conn.commit()

# c.execute("SELECT * FROM users")

# print(c.fetchall())

# allways close connection
conn.close()
