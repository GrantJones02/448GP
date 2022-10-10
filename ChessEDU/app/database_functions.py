import sqlite3
from objects import User
import os
from pathlib import Path

# Databse global string

CRED_DATABASE = str(Path(f"{os.getcwd()}").parents[0])+os.path.sep+"deployment"+os.path.sep+"databases"+os.path.sep+"sqlite3"+os.path.sep+"chessEDU_credentials.db"
MOD_DATABASE = str(Path(f"{os.getcwd()}").parents[0])+os.path.sep+"deployment"+os.path.sep+"databases"+os.path.sep+"sqlite3"+os.path.sep+"chessEDU_modules.db"

#------------------------------------------------------------------------------#

### Login Process Functions ###
def get_user_by_id(user_id):
    # Connects with DB
    conn = sqlite3.connect(CRED_DATABASE)
    curs = conn.cursor()
    # Gets entire user profile based on ID
    curs.execute("select * from users where userid=(?);", [user_id])
    response_user = curs.fetchone()
    conn.commit()
    conn.close()
    # If either query returns no results, user does not exist
    if response_user is None:
        return None
    else:
        # Use the User class in objects file to create a User session
        courses = []
        if response_user[5] is not None:
            for course_id in response_user[5].split(','):
                courses.append(int(course_id))
        return User(response_user[0], response_user[1], response_user[2], response_user[3], response_user[4], courses)

def get_details_by_username(username):
    conn = sqlite3.connect(CRED_DATABASE)
    curs = conn.cursor()
    curs.execute("select * from users where username = (?);", [username])
    user_details = curs.fetchone()
    conn.commit()
    conn.close()
    return(user_details)

#------------------------------------------------------------------------------#

### Admin Page Functions ###
'''
    function : admin_user_data
    params : none
    returns : list of user lists [[str(username), tuple(id, role, last login)], ...]
    descr. : connect with the app database to return a dictionary of users
'''
def admin_user_data():
    admin_user_data = []
    conn = sqlite3.connect(CRED_DATABASE)
    curs = conn.cursor()
    curs.execute("select username from users;")
    user = curs.fetchone()

    while(user is not None):
        admin_user_data.append([user[0]])
        user = curs.fetchone()

    index = 0
    for user in admin_user_data:
        curs.execute("select id,role,lastlogin from users where userid=(select id from users where username=(?));", [user[0]])
        admin_user_data[index].append(curs.fetchone())
        index += 1
    conn.commit()
    conn.close()
    return(admin_user_data)

'''
    function : update_user_permissions
    params: users, new_roles
    returns : none
    descr. : connect with the app database to update user permissions
'''
def set_admin(user_id):
    conn = sqlite3.connect(CRED_CRED_DATABASE)
    curs = conn.cursor()
    curs.execute("update users set role=(?) where userid=(?)", [0, user_id])
    conn.commit()
    conn.close()

'''
    function : delete_users
    params: users
    returns : none
    descr. : connect with the app database to erase a user from the application
'''
def delete_users(users):
    conn = sqlite3.connect(CRED_DATABASE)
    curs = conn.cursor()
    for user in users:
        curs.execute("delete from users where username=(?);", [user])
    conn.commit()
    conn.close()

'''
    function : create_new_user
    params: user - Dict: {"new_username": str, "new_password": str, "role", 0/1}
    returns : none
    descr. : connect with the app database to create a new user
'''
def create_new_user(user):
    conn = sqlite3.connect(CRED_DATABASE)
    curs = conn.cursor()
    curs.execute("select * from users where username=(?);", [user["new_username"]])
    existinguser = curs.fetchone()
    if existinguser == None:
        # sqlite execute function takes a list as a parameter, so put new user values in a list
        new_user = []
        # New id
        curs.execute("select max(id) from users;")
        new_id = 1 + curs.fetchone()[0]
        new_user.append(new_id)
        # New username
        new_user.append(user["new_username"])
        # New password
        new_user.append(user["new_password"])
        # New roles
        new_user.append(user["role"])
        # Last Login is undefined
        new_user.append("------")
        # Add user to users table
        curs.execute("insert into users values ((?), (?), (?), (?), (?));", new_user)
    else:
        conn.close()
        raise
    conn.commit()
    conn.close()
