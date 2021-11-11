# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

""" Blogs Database """

import sqlite3
import random

DB_FILE = "discobandit.db"

def create_db():
    ''' Creates / Connects to DB File '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, entryname TEXT, content TEXT);")
    # c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, id INTEGER, content TEXT);")
    db.close()


def create_blog(title,text,username, entryname):
    ''' Publishes a blog '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("INSERT INTO blogs VALUES (?, ?, ?, ?);", (username, title, entryname, text))

    db.commit()

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    db.commit()



def update_blog(username,entryname,text):
    ''' Updates blog '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO blogs VALUES (?, ?, ?, ?);", (username, title, entryname, text))
    db.commit()

    return True

def edit_blog(username, title, oldentryname, newentryname, text):
    '''Edit existing blog'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE blogs SET entryname = \"" + newentryname + "\", content = \"" + text + "\" WHERE usernames = \"" + username + "\" AND blognames = \"" + title + "\" AND entryname = \"" + oldentryname + "\";")
    db.commit()

    return True

def delete_blog(blogtitle):
    ''' Delete blog '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM blogs WHERE blognames = '" + str(blogtitle) + "'")
    db.commit()

    return True


def fetch_blogs():
    ''' Fetch list of blog names '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM blogs")
    blogs = []
    users = []
    for a_tuple in c.fetchall():
        if a_tuple[1] not in blogs:
            blogs.append(a_tuple[1])
            users.append(a_tuple[0])

    # reverse so most recent blogs show up
    blogs.reverse()
    users.reverse()
    return zip(blogs,users)


def fetch_user_blogs(username):
    ''' Fetch list of a USER's blog names '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM blogs")
    blogs = []
    for a_tuple in c.fetchall():
        if a_tuple[0] == username and a_tuple[1] not in blogs:
            blogs.append(a_tuple[1])

    return blogs

def get_user_from_title(blogtitle):
    ''' Fetch user from blog title'''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM blogs")
    for a_tuple in c.fetchall():
        if a_tuple[1] == blogtitle:
            return a_tuple[0]
    return -1

def fetch_entry_names(blogtitle):
    ''' retrieves all entries names in database that belongs to the specified
        blog (has the specified blog title) '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT entryname FROM blogs WHERE blognames = '" + blogtitle + "'")
    names = []
    for a_tuple in c.fetchall():
        names.append(a_tuple[0])
    names.reverse()
    return names

def fetch_entry_contents(blogtitle):
    ''' retrieves all entries names in database that belongs to the specified
        blog (has the specified blog title) '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT content FROM blogs WHERE blognames = '" + blogtitle + "'")
    contents = []
    for a_tuple in c.fetchall():
        contents.append(a_tuple[0])
    contents.reverse()
    return contents


def auth_blog(method,title,entryname,text):
    ''' Checks if the user created a valid blog '''

    isempty = not method or not title or not entryname or not text

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM blogs")
    blogs = []
    for a_tuple in c.fetchall():
        blogs.append(a_tuple[1])

    if isempty or title in blogs:
        return False
    return True

def auth_entry(method,title,entryname,text):
    ''' Checks if the user created a valid blog '''

    isempty = not method or not title or not entryname or not text

    if isempty:
        return False
    return True

# TESTS
create_db()

# db = sqlite3.connect(DB_FILE)
# c = db.cursor()
# c.execute("SELECT * FROM blogs")
# print(c.fetchall())
# print("\n\n\n")
# delete_blog("christmas")
# c.execute("SELECT * FROM blogs")
# print(c.fetchall())
