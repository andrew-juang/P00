# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

"""Handles all of the routes of the Flask Application"""

from flask import Flask, render_template, request, session, redirect, url_for

from app import app
from app.auth import auth_user, create_user, create_db


@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    """ Display login page if there is no username in session, else display the
       response with the session username passed in. """

    # Renders response if there is a user logged in.
    if 'username' in session:
        return render_template('response.html',username=session['username'])
    return render_template('login.html')

# authetication of login
@app.route("/auth", methods=['GET','POST'])
def authenticate():
    """ Checks whether method is get, post. If get method, then redirect to
       loginpage. If post, then authenticate the username and password, rendering
       the error page if incorrect and the response.html if correct username/pass. """

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
        return render_template('response.html', username=session['username'])
    elif auth_state == "bad_pass":
        return render_template('login.html', input='Password is ')
    elif auth_state == "bad_user":
        return render_template('login.html', input='Username is ')

@app.route("/register")
def register():
    #displays register page
    return render_template('register.html')

# authetication of username and passwords given in register page from user
@app.route("/rAuth", methods =['GET', 'POST'])
def rAuthenticate():
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
    """ Logout user by deleting user from session dict. Redirects to loginpage """

    # Delete user. This try... except... block prevent an error from ocurring when the logout page is accessed from the login page
    try:
        session.pop('username')
    except KeyError:
        return redirect(url_for('disp_loginpage'))
    # Redirect to login page
    return redirect(url_for('disp_loginpage'))


@app.route("/create")
def create():
    return render_template('create.html')
