# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

""" Handles all of the routes of the Flask Application """

from flask import Flask, render_template, request, session, redirect, url_for

from app import app
from app.auth import auth_user, create_user, create_db
from app.blogs import create_blog, update_blog, delete_blog, fetch_blogs, get_title_from_id, get_content_from_id, get_ids, fetch_users

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    ''' Display login page if there is no username in session, else display the
       response with the session username passed in. '''

    # Renders response if there is a user logged in, else render login page
    if 'username' in session:
        blogs = fetch_blogs()
        users = fetch_users()
        return render_template('response.html',username=session['username'], blogs_users=zip(blogs,users))
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
        return redirect(url_for('disp_loginpage'))

    auth_state = auth_user(username, password)
    if auth_state == True:
        session['username'] = username
        return redirect(url_for('disp_loginpage'))
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
        return redirect(url_for('disp_loginpage'))
    # Redirect to login page
    return redirect(url_for('disp_loginpage'))


@app.route("/create", methods=['GET','POST'])
def create():
    ''' Displays create blog page '''

    # user is logged in and is allowed to create
    if 'username' in session:
        return render_template('create.html')
    # user is not logged in and redirected to login page (catches error when user tries to go directly to /create w/o logging in)
    else:
        return redirect(url_for('disp_loginpage'))


@app.route("/createblog", methods=['GET', 'POST'])
def createblog():
    ''' Creates blog '''

    method = request.method
    title = request.form.get('Title')
    entryname = request.form.get('Entryname')
    text = request.form.get('Body')

    # TODO: CHECK if field is empty
    if method == 'POST':
        create_blog(title,text,session['username'],entryname)

    return redirect(url_for('disp_loginpage'))

@app.route("/dashboard/<username>", methods=['GET', 'POST'])
def dashboard(username):
    ''' route for displaying a blog page '''

    if not bool(username):
        return redirect(url_for('dashboard', username=session['username']))
    titles = []
    content = []
    ids = []
    print(username)

    ids = get_ids(username)
    print(ids)
    for id in ids:
        titles.append(get_title_from_id(id))

    # displays the blog with title and content using display template
    return render_template('display.html', user = username, titles = titles)


@app.route("/display/<blogtitle>", methods=['GET', 'POST'])
def displayblog(blogtitle):
    ''' Display a blog and each of its entries '''

    return
