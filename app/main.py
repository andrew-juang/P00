# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Thingamablog

""" Handles all of the routes of the Flask Application """

from flask import Flask, render_template, request, session, redirect, url_for

from app import app
from app.auth import auth_user, create_user, create_db
from app.blogs import ( create_blog, update_blog, delete_blog, fetch_blogs, fetch_entry_names, fetch_entry_contents,
                        fetch_user_blogs, get_user_from_title, delete_blog, auth_blog, auth_entry, edit_blog)

@app.route("/", methods=['GET', 'POST'])
def index():
    ''' Display login page if there is no username in session, else display the
       response with the session username passed in. '''

    # Renders response if there is a user logged in, else render login page
    if 'username' in session:
        blogs = fetch_blogs()
        return render_template('response.html',username=session['username'], blogs_users=blogs)
    return render_template('login.html')


# authetication of login
@app.route("/auth", methods=['GET','POST'])
def authenticate():
    ''' Checks whether method is get, post. If get method, then redirect to
       loginpage. If post, then authenticate the username and password, rendering
       the error page if incorrect and the response.html if correct username/pass. '''

    # Variables
    method = request.method
    username = request.form.get('username')
    password = request.form.get('password')

    # Get vs Post
    if method == 'GET':
        return redirect(url_for('index'))

    auth_state = auth_user(username, password)
    if auth_state == True:
        session['username'] = username
        return redirect(url_for('index'))
    elif auth_state == "bad_pass":
        return render_template('login.html', input="bad_pass")
    elif auth_state == "bad_user":
        return render_template('login.html', input="bad_user")


@app.route("/register")
def register():
    ''' Displays register page '''

    return render_template('register.html')


@app.route("/rAuth", methods =['GET', 'POST'])
def rAuthenticate():
    ''' Authentication of username and passwords given in register page from user '''

    method = request.method
    username = request.form.get('username')
    password0 = request.form.get('password0')
    password1 = request.form.get('password1')

    if method == 'GET':
        return redirect(url_for('register'))

    if method == 'POST':
        # error when no username is inputted
        if len(username) == 0:
            return render_template('register.html', given = "username")
        # error when no password is inputted
        elif len(password0) == 0:
            return render_template('register.html', given = "password")
        elif len(password0) < 8:
            return render_template('register.html', given = "password greater than 8 characters")
        # a username and password is inputted
        # a username and password is inputted
        else:
            # if the 2 passwords given don't match, will display error saying so
            if password0 != password1:
                return render_template('register.html', mismatch = True)
            else:
                # creates user account b/c no fails
                if create_user(username, password0):
                    return render_template('login.html', input='success')
                # does not create account because create_user failed (username is taken)
                else:
                    return render_template('register.html', taken = True)


@app.route("/logout")
def logout():
    ''' Logout user by deleting user from session dict. Redirects to loginpage '''

    # Delete user. This try... except... block prevent an error from ocurring when the logout page is accessed from the login page
    try:
        session.pop('username')
    except KeyError:
        return redirect(url_for('index'))
    # Redirect to login page
    return redirect(url_for('index'))


@app.route("/create", methods=['GET','POST'])
def create():
    ''' Displays create blog page '''

    # user is logged in and is allowed to create
    if 'username' in session:
        return render_template('create.html', username=session['username'])
    # user is not logged in and redirected to login page (catches error when user tries to go directly to /create w/o logging in)
    else:
        return redirect(url_for('index'))


@app.route("/createblog", methods=['GET', 'POST'])
def createblog():
    ''' Creates blog '''

    method = request.method
    title = request.form.get('Title')
    entryname = request.form.get('Entryname')
    text = request.form.get('Body')

    # CHECK if any field is empty and throws and error
    if auth_blog(method,title,entryname,text) and method == 'POST':
        create_blog(title,text,session['username'],entryname)
    else:
        blogs = fetch_blogs()
        return render_template('response.html',username=session['username'], blogs_users=blogs, input="Invalid Blog")

    return redirect(url_for('index'))


@app.route("/dashboard/<username>", methods=['GET', 'POST'])
def dashboard(username):
    ''' Route for displaying a user's dashboard '''

    titles = fetch_user_blogs(username)
    titles.reverse()

    # displays the dashboard with title and content using dashboard template
    return render_template('dashboard.html', user = username, titles = titles, username=session['username'])


@app.route("/display/<blogtitle>", methods=['GET', 'POST'])
def displayblog(blogtitle):
    ''' Display a blog and each of its entries '''

    # retrieves all entries associated with the blog
    entrynames = fetch_entry_names(blogtitle)
    print(entrynames)
    entrycontents = fetch_entry_contents(blogtitle)
    is_own_page = (session['username'] == get_user_from_title(blogtitle))

    # displays blog with entry names and content using display template
    return render_template('display.html', blogtitle = blogtitle,
                                           entries = zip(entrynames, entrycontents),
                                           is_own_page=is_own_page,
                                           username=session['username'])


@app.route("/addentry", methods=['GET', 'POST'])
def addentry():
    ''' Displays Create Entry Page'''

    title = request.form.get('Blogtitle')
    print("SDKLJFSKLDFJLSKDJFLJK")
    print(title)
    # user is logged in and is allowed to create
    if 'username' in session:
        return render_template('createentry.html', blogtitle=title, username=session['username'])
    # user is not logged in and redirected to login page (catches error when user tries to go directly to /create w/o logging in)
    else:
        return redirect(url_for('index'))


@app.route("/createentry", methods=['GET', 'POST'])
def createentry():
    ''' Creates an Entry '''

    method = request.method
    title = request.form.get('Blogtitle')
    entryname = request.form.get('Entryname')
    text = request.form.get('Body')

    if auth_entry(method,title,entryname,text) and method == 'POST':
        create_blog(title,text,session['username'],entryname)
        return redirect(url_for('displayblog', blogtitle=title))
    else:
        # retrieves all entries associated with the blog
        entrynames = fetch_entry_names(title)
        entrycontents = fetch_entry_contents(title)
        is_own_page = (session['username'] == get_user_from_title(title))

        # displays blog with entry names and content using display template
        return render_template('display.html', blogtitle = title,
                                               entries = zip(entrynames, entrycontents),
                                               is_own_page = is_own_page,
                                               input = "Invalid Entry" )


@app.route("/deleteblog", methods=['GET', 'POST'])
def deleteblog():
    ''' Delete a blog '''

    title = request.form.get('blogtitle')
    delete_blog(title)

    return redirect(url_for('index'))


@app.route("/editentry", methods=['GET', 'POST'])
def editentry():
    '''Display edit entry page'''

    title = request.form.get('blogtitle')
    print(title)
    entryname = request.form.get('Entryname')
    print(entryname)
    entrycontents = request.form.get('content')
    print(entrycontents)

    if 'username' in session:
        return render_template('editentry.html', blogtitle=title, username=session['username'], entryname=entryname, entrycontents=entrycontents)
    else:
        return redirect(url_for('index'))


@app.route("/updateentry", methods=['GET', 'POST'])
def updateentry():
    ''' Updates an entry '''

    method = request.method

    title = request.form.get('Blogtitle')
    print(title)
    oldentryname = request.form.get('Oldentryname')
    print(oldentryname)
    newentryname = request.form.get('Entryname')
    print(newentryname)
    text = request.form.get('Body')
    print(text)
    print("username: " + session['username'])

    #if auth_entry(method,title,newentryname,text) and method == 'POST':
    edit_blog(session['username'], title, oldentryname, newentryname, text)
    return redirect(url_for('displayblog', blogtitle=title))
