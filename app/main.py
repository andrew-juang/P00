# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

"""Handles all of the routes of the Flask Application"""

from flask import Flask, render_template, request, session, redirect, url_for

from app import app
from app.auth import auth_user, create_user

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
    if method == 'POST':
        # Displays corresponding error message
        if username != 'eric' and password != 'guo':
            return render_template('login.html',input='Username and password are ')
        elif username != 'eric':
            return render_template('login.html',input='Username is ')
        elif password != 'guo':
            return render_template('login.html',input='Password is ')
        else:
            session['username'] = 'eric'
            return render_template('response.html',username=session['username'])

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
        # if the 2 passwords given don't match, will display error saying so
        if password0 != password1:
            return render_template('register.html', mismatch = True)
        else:
            return render_template('login.html')
            '''commented out b/c create_user does not work, gives error that 
                                    "SQLite objects created in a thread can only be used in that same thread"
                                    
            # creates user account b/c no fails (pass match, username not taken)
            if create_user(username, password0):
                return render_template('login.html')
            # username is taken, account creation fails, display such error
            else:
                return render_template('register.html', taken = True)
            '''
    
    

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
