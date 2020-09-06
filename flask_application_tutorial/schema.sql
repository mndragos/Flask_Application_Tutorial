DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS articles;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    register_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')));

CREATE TABLE articles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    body TEXT NOT NULL,
    create_date DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')));