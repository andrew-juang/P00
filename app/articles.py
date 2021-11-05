# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

""" Article Database """

import sqlite3

DB_FILE = "discobandit.db"

def create_db():
    ''' Creates / Connects to DB File '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, id INTEGER, content TEXT);")
    db.close()


def create_blog():
    ''' Adds user to database if right username and password are given when a
        person registers '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # add more conditionals here
    # username is taken already, returns fail to display error
    c.execute("SELECT usernames FROM users")
    users = []
    for a_tuple in c.fetchall():
        users.append(a_tuple[0])

    # change this into separate function to check requirements
    if username in users:
        return False
    # username is not taken, creates account with given username and password
    else:
        c.execute("INSERT INTO users VALUES (?, ?);", (username, password))
        db.commit()
        return True


db = sqlite3.connect(DB_FILE)
c = db.cursor()
db.commit()
c.execute("SELECT usernames FROM blogs")
blogs = []
for a_tuple in c.fetchall():
    blogs.append(a_tuple[0])
print(blogs)
