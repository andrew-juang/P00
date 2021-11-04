# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

"""Authentication/Creation of Users"""

import sqlite3

DB_FILE="discobandit.db"

def auth_user(username, password):
    """ Validates a username + password when person logs in """

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (usernames TEXT, passwords TEXT);")

    c.execute("SELECT usernames FROM users")
    if username in c.fetchall():
        return True
    return True

    db.commit()
    db.close()


def create_user(username, password):
    """ Adds user to database if right username and password are given when a
        person registers """

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (usernames TEXT, passwords TEXT);")

    # add more conditionals here
    print(username in c.fetchall())
    # username is taken already, returns fail to display error
    # NEED TO FIX THIS CONDITIONAL
    if username in c.fetchall():
        return False
    # username is not taken, creates account with given username and password
    else:
        c.execute("INSERT INTO users(usernames,passwords) VALUES (?, ?)", (username,password))
        c.execute("SELECT * FROM users")
        print(c.fetchall())
        db.commit()
        db.close()
        return True
    # c.execute("SELECT * FROM users")
