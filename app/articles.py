# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

""" Article Database """

import sqlite3
import random

DB_FILE = "discobandit.db"

def create_db():
    ''' Creates / Connects to DB File '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS blogs (usernames TEXT, blognames TEXT, id INTEGER, content TEXT);")
    db.close()


def create_blog(title,text,username):
    ''' Publishes a blog '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    id = generate_id()
    c.execute("INSERT INTO blogs VALUES (?, ?, ?, ?);", (username, title, id, text))

    db.commit()

def generate_id():
    ''' Generate random ID for user '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    id = random.randint(0,999999)
    c.execute("SELECT id FROM blogs")
    blogids = []
    for a_tuple in c.fetchall():
        blogids.append(a_tuple[0])
    while id in blogids:
        id = random.randint(0,999999)
    return id


def update_blog():
    ''' Updates blog '''

    return True


def delete_blog():
    ''' Delete blog '''

    return True


def fetch_blogs():
    ''' Fetch list of blog names '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT blognames FROM blogs")
    blogs = []
    for a_tuple in c.fetchall():
        blogs.append(a_tuple[0])
    return blogs


def get_ids(username):
    ''' Returns the blog ids of the user '''

    ids = []
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM blogs")
    for a_tuple in c.fetchall():
        if(a_tuple[0] == username):
            ids.append(a_tuple[2])
    return ids;

def get_title_from_id(blogID):
    ''' returns the title of corrresponding blog using the blog id '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT blognames FROM blogs WHERE id = "+ str(blogID))
    for content in c.fetchall():
        return content[0]


def get_content_from_id(blogID):
    ''' returns the content of corrresponding blog using the blog id '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT content FROM blogs WHERE id = "+ str(blogID))
    for content in c.fetchall():
        return content[0]

def fetch_users():
    ''' Returns list of users '''

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT usernames FROM blogs")
    users = []
    for a_tuple in c.fetchall():
        users.append(a_tuple[0])
    return users


# TESTS
create_db()
db = sqlite3.connect(DB_FILE)
c = db.cursor()
db.commit()
c.execute("SELECT * FROM blogs")
print(c.fetchall())
blogs = []
for a_tuple in c.fetchall():
    blogs.append(a_tuple[0])
print(blogs)
