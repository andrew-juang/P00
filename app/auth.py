# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

"""Authentication/Creation of Users"""

import sqlite3

DB_FILE="discobandit.db"

def auth_user():
    """ Validates a username + password when person registers """

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (usernames TEXT, passwords TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, id INTEGER, content TEXT);")

    # Put a bunch of conditionals here validating the username and password
    #
    #
    #
    #

    # add stuff

def create_user():
    """ Adds user to database if right username and password are given """
