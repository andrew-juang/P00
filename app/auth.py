# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

"""Authentication/Creation of Users"""

import sqlite3

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (usernames TEXT, passwords TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, id INTEGER, content TEXT);")

def auth_user(username, password):
    """ Validates a username + password when person registers """

    c.execute("SELECT usernames FROM users")
    if username in c.fetchall():
        #


def create_user(username, password):
    """ Adds user to database if right username and password are given """

    c.execute("SELECT usernames FROM users")

    # add more conditionals here
    if username in c.fetchall():
        return False
    else:
        c.execute("INSERT INTO users VALUES (?, ?);",(username,password))
    c.execute("SELECT * FROM users")
    print(c.fetchall())
