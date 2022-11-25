## Flask Packages ##
from flask import Flask, flash, render_template, redirect, request, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
## Remove in produciton, just allows to run and access on local device
from flask_cors import CORS
## Relative import for forms and objects used in the app ##
from forms import login_form, signup_form
from user import User
from account_manager import AccountManager
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

# Manager objects
account_manager = AccountManager()

'''
    function: load_user
    param: user_id (int)
    return: user object (class)
    descr.: required by flask-login
'''
@login_manager.user_loader
def load_user(user_id):
    user_info = account_manager.get_user_by_id(user_id)
    return(User(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4]))

### Routes ###
'''
 function : home
 param : none
 return : render template
 descr : landing page after logging in, renders home page
'''
@app.route('/', methods=["GET"])
def home():
    # Renders landing page on initial load
    return render_template("base.html", logged_in=current_user.is_authenticated)

'''
    function : login
    param : none
    return : renders either landing page if user is authenticated, otherwise loads the register or authenticated routes based on submitted form
    descr. : Connects with SQLite3 DB for the app and validates user login
'''
@app.route('/login', methods=["GET"])
def login():
    user_signup_form = signup_form()
    user_login_form = login_form()
    # Session management feature : loads landing page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Load login page on load AND failed login
    return render_template('login.html', signup_form=user_signup_form, login_form=user_login_form, logged_in=current_user.is_authenticated)

'''
    function : register
    param : none
    return : renders the login page or redirects to home if user is already logged in or successfully registers
    descr. : Connects with SQLite3 DB for the app and validates user sign up
'''
@app.route('/register', methods=["POST"])
def register():
    user_signup_form = signup_form()
    user_login_form = login_form()
    if user_signup_form.validate_on_submit():
        print("In signup validate")
        if user_signup_form.new_name.data != "" and user_signup_form.new_name.data != None:
            print("new username is not none")
            if user_signup_form.new_pass.data == user_signup_form.confirm_pass.data:
                print("passwords match")
                if len(user_signup_form.new_pass.data) >= 12:
                    print("password >= 12")
                    uppers, lowers, specials, digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "!@#$%^&*", "0123456789"
                    u, l, s, d = 0, 0, 0, 0
                    for char in user_signup_form.new_pass.data:
                        if char in uppers:
                            u += 1
                        if char in lowers:
                            l += 1
                        if char in specials:
                            s += 1
                        if char in digits:
                            d += 1
                    if u >= 1 and l >= 1 and s >= 1 and d >= 1 and u+l+s+d==len(user_signup_form.new_pass.data):
                        print("strong password")
                        new_user = {
                            "new_username": user_signup_form.new_name.data,
                            "new_password": user_signup_form.new_pass.data,
                            "role": 1
                        }
                        try:
                            print("creating user")
                            account_manager.create_new_user(new_user)
                            flash("Signup successful! Attempting first login...")
                        except Exception as e:
                            print(e)
                            flash("An error occurred while attempting to create your account.")
                    else:
                        flash("Password must contain at least one lowercase letter, uppercase letter, number, and special character (!@#$%^&*)!")
                else:
                    flash("Password must be at least 12 characters long!")
            else:
                flash("Passwords entered must match!")
        else:
            flash("Username cannot be blank!")
        user_details = account_manager.get_details_by_username(user_signup_form.new_name.data)
        if user_details is not None:
            # Creates user (returned from load_user)
            User = load_user(user_details[0])
            # Checks if the entered data matches the db data
            if user_signup_form.new_name.data == User.username and user_signup_form.new_pass.data == User.password:
                # Login user and render landing page
                login_user(User)
                session.permanent = True
                flash("Login successful!")
                return redirect(url_for('home'))
    # Load login page on load AND failed login
    return render_template('login.html', signup_form=user_signup_form, login_form=user_login_form, logged_in=current_user.is_authenticated)

'''
    function : authenticate
    param : none
    return : renders the login page or redirects to home if user is already logged in or successfully logs in
    descr. : Connects with SQLite3 DB for the app and validates user login
'''
@app.route('/authenticate', methods=["POST"])
def authenticate():
    user_signup_form = signup_form()
    user_login_form = login_form()
    # Session management feature : loads landing page if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if user_login_form.validate_on_submit():
        user_details = account_manager.get_details_by_username(user_login_form.username.data)
        if user_details is not None:
            # Creates user (returned from load_user)
            User = load_user(user_details[0])
            # Checks if the entered data matches the db data
            if user_login_form.username.data == User.username and user_login_form.password.data == User.password:
                # Login user and render landing page
                login_user(User)
                session.permanent = True
                return redirect(url_for('home'))
    # Load login page on load AND failed login
    return render_template('login.html', signup_form=user_signup_form, login_form=user_login_form, logged_in=current_user.is_authenticated)

'''
    function : logout
    param : none
    return : logs current user out and renders login page
    descr. : Uses flask_login.logout_user() to end session
'''
@app.route('/logout', methods=('GET', 'POST'))
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))

'''
    function : account
    params : None
    return : Renders the board page
    descr. : Directs the user to a page with their account information displayed.
'''
@app.route('/account', methods=('GET', 'POST'))
def account():
    if current_user.is_authenticated:
        return render_template("account.html", logged_in=current_user.is_authenticated)
    return redirect(url_for('home'))

'''
    function : catalog
    params : None
    return : Renders the course catalog page
    descr. : Directs the user to a page that lists available courses.
'''
@app.route('/catalog', methods=('GET', 'POST'))
def catalog():
    return render_template("catalog.html", logged_in=current_user.is_authenticated)

'''
    function : course
    params : id
    return : Renders the directed course's page
    descr. : Directs the user to the page they navigated to.
'''
@app.route('/course/<page>', methods=['GET'])
def course(page):
    return render_template(f"courses/{page}.html", logged_in=current_user.is_authenticated)

'''
    function : board
    params : None
    return : Renders the board page
    descr. : Directs the user to a interactive chessboard page.
'''
@app.route('/board', methods=('GET', 'POST'))
def board():
    return render_template("board.html", logged_in=current_user.is_authenticated)

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
#             return render_template("admin.html", userData=account_manager.admin_user_data())
#         elif request.method == "POST":
#             # Do something
#             return render_template("admin.html", userData=account_manager.admin_user_data())
#         else:
#             return redirect(url_for('home'))

### Private functions ###
# '''
#     function:
#     params:
#     return:
#     descr.:
# '''

if __name__ == "__main__":
    app.run()
