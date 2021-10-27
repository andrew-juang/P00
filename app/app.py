# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo
# SoftDev
# P00 -- Web Log Hosting Site
# 2021-10-27

from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for

# Flask app instance
app = Flask(__name__)

# Secret key for session
app.secret_key = urandom(32)


@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    ''' Display login page if there is no username in session, else display the
        response with the session username passed in.'''

    # Renders response if there is a user logged in.
    if 'username' in session:
        return render_template('response.html',username=session['username'])
    return render_template('login.html')

@app.route("/auth", methods=['GET','POST'])
def authenticate():
    ''' Checks whether method is get, post. If get method, then redirect to
        loginpage. If post, then authenticate the username and password, rendering
        the error page if incorrect and the response.html if correct username/pass.'''

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

@app.route("/logout")
def logout():
    ''' Logout user by deleting user from session dict. Redirects to loginpage'''

    # Delete user. This try... except... block prevent an error from ocurring when the logout page is accessed from the login page
    try:
        session.pop('username')
    except KeyError:
        return redirect(url_for('disp_loginpage'))
    # Redirect to login page
    return redirect(url_for('disp_loginpage'))

if __name__ == "__main__":
    app.debug = True
    app.run()
