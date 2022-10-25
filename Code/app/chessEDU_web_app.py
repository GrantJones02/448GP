## Flask Packages ##
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
## Remove in produciton, just allows to run and access on local device
from flask_cors import CORS
## Relative import for forms and objects used in the app ##
from forms import login_form
from objects import User
import database_functions as db
## Other packegs for avrious other functionality ##
import sqlite3
import secrets
from datetime import timedelta

app = Flask(__name__)
# Secret key used for session encryption, randomly generated on each run
app.config['SECRET_KEY'] = secrets.token_hex()
# Session timeout of 20 minutes
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)
# User login features
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Temporary features for dev. environment
CORS(app)

'''
    function: load_user
    param: user_id (int)
    return: user object (class)
    descr.: required by flask-login
'''
@login_manager.user_loader
def load_user(user_id):
    return(db.get_user_by_id(user_id))

### Routes ###
'''
 function : home
 param : none
 return : render template
 descr : landing page after logging in, renders home page
'''
@app.route('/', methods=('GET', 'POST'))
@login_required
def home():
    # Renders landing page on initial load
    return render_template("home.html")

'''
    function : login
    param : none
    return : renders either landing page or login page depending upon login status
    descr. : Connects with SQLite3 DB for the app and validates user login
'''
@app.route('/login', methods=("GET", "POST"))
def login():
    # Session management feature : loads landing page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Form from forms file
    user_login_form = login_form()
    if user_login_form.validate_on_submit():
        user_details = db.get_details_by_username(user_login_form.username.data)
        if user_details is not None:
            # Creates user (returned from load_user)
            User = load_user(user_details[0])
            # Checks if the entered data matches the db data
            if user_login_form.username.data == User.username and user_login_form.password.data == User.password:
                # Login user and render landing page
                login_user(User)
                session.permanent = True
                flash("Login successful!")
                return redirect(url_for('home'))
    # Load login page on load AND failed login
    return render_template('login.html', form=user_login_form)

'''
    function : logout
    param : none
    return : logs current user out and renders login page
    descr. : Uses flask_login.logout_user() to end session
'''
@app.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

'''
    function : courses
    params : None
    return : Renders the courses page
    descr. : Directs the user to a page that lists available courses.
    Login required
'''
@app.route('/course', methods=('GET', 'POST'))
@login_required
def courses():
    return render_template("course.html")

'''
    function : board
    params : None
    return : Renders the board page
    descr. : Directs the user to a interactive chessboard page.
    Login required
'''
@app.route('/board', methods=('GET', 'POST'))
@login_required
def board():
    return render_template("board.html")

# '''
#     function : account
#     params : None
#     return : Renders the board page
#     descr. : Directs the user to a page with their account information displayed.
#     Login required
# '''
# @app.route('/account', methods=('GET', 'POST'))
# @login_required
# def account():
#     return render_template("account.html")

# '''
#     function : admin
#     param : none
#     return : Renders the admin page
#     descr. : Handles input from the user manage individual user permissions.
#     Login required
# '''
# @app.route('/~admin', methods=('GET', 'POST'))
# @login_required
# def admin():
#     if not current_user.get_admin():
#         return redirect(url_for('unauthorized'))
#     else:
#         if request.method == "GET":
#             return render_template("admin.html", userData=db.admin_user_data())
#         elif request.method == "POST":
#             # Do something
#             return render_template("admin.html", userData=db.admin_user_data())
#         else:
#             return redirect(url_for('home'))

# '''
#     function : unauthorized
#     param : none
#     return : Renders the unauthorized page
#     descr. : Redirects a user to this page when they attempt to access pages without required permissions.
#     Login required
# '''
# @app.route('/unauthorized', methods=('GET', 'POST'))
# @login_required
# def unauthorized():
#     return render_template("unauth.html")



### Private functions ###
# '''
#     function:
#     params:
#     return:
#     descr.:
# '''

if __name__ == "__main__":
    app.run()