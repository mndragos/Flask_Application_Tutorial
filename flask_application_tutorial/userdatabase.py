import sqlite3


# connect to database
conn = sqlite3.connect("userdata.db")


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))


# create rows
conn.row_factory = make_dicts

# create a cursor
c = conn.cursor()

# create a table for users
# c.execute(
#     """ CREATE TABLE users(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL,
#     username VARCHAR(30) NOT NULL,
#     password VARCHAR(100) NOT NULL,
#     register_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
# )
# """
# )

# # # # create a table for articles
# c.execute(
#     """ CREATE TABLE articles(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title VARCHAR(255) NOT NULL,
#     author VARCHAR(100) NOT NULL,
#     body TEXT NOT NULL,
#     create_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
# )
# """
# )

# commit changes
# conn.commit()

# c.execute("SELECT * FROM users")
c.execute("SELECT * FROM articles")
rez = c.fetchall()

for row in range(len(rez)):
    print(rez[row]["id"], rez[row]["title"], rez[row]["author"])

# allways close connection
conn.close()
