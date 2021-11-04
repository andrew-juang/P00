# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

"""Authentication/Creation of Users"""

import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

DB_FILE = "discobandit.db"

def create_db():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (usernames TEXT, passwords TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, id INTEGER, content TEXT);")
    db.close()

def auth_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    """ Validates a username + password when person logs in """

    c.execute("SELECT usernames FROM users")
    users = []
    for a_tuple in c.fetchall():
        users.append(a_tuple[0])

    if username in users:
        c.execute("SELECT passwords FROM users WHERE usernames = '" + username + "'")
        if c.fetchall()[0][0] == password:
            session['username'] = username
            return render_template('response.html', username=session['username'])
        else:
            return render_template('login.html', input='Password is ')
    else:
        return render_template('login.html', input='Username is ')


def create_user(username, password):
    """ Adds user to database if right username and password are given when a
        person registers """

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # add more conditionals here
    # username is taken already, returns fail to display error
    c.execute("SELECT usernames FROM users")
    users = []
    for a_tuple in c.fetchall():
        users.append(a_tuple[0])

    # change this into separate function to check requirements
    if username in users or len(username)<1 or len(password)<1:
        return False
    # username is not taken, creates account with given username and password
    else:
        c.execute("INSERT INTO users VALUES (?, ?);", (username, password))
        db.commit()

create_db()

db = sqlite3.connect(DB_FILE)
c = db.cursor()
db.commit()
c.execute("SELECT usernames FROM users")
users = []
for a_tuple in c.fetchall():
    users.append(a_tuple[0])
print(users)
