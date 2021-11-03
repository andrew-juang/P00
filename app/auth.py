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
    """ Validates a username + password when person logs in """

    c.execute("SELECT usernames FROM users")
    if username in c.fetchall():
        return True
        

def create_user(username, password):
    """ Adds user to database if right username and password are given when a
        person registers """

    c.execute("SELECT usernames FROM users")

    # add more conditionals here
    
    # username is taken already, returns fail to display error
    if username in c.fetchall():
        return False
    # username is not taken, creates account with given username and password
    else:
        c.execute("INSERT INTO users VALUES (?, ?);",(username,password))
       
    c.execute("SELECT * FROM users")
    print(c.fetchall())
    
