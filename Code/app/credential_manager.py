import os
import sqlite3
from pathlib import Path
from datetime import date

class CredentialManager():
    def __init__(self):
        self._CRED_DB = str(Path(f"{os.getcwd()}").parents[0])+os.path.sep+"deployment"+os.path.sep+"databases"+os.path.sep+"sqlite3"+os.path.sep+"chessEDU_credentials.db"

    ### Sign Up Process Functions ###
    '''
        function : create_new_user
        params: user - Dict: {"new_username": str, "new_password": str, "role", 0/1}
        returns : none
        descr. : connect with the app database to create a new user
    '''
    def create_new_user(self, user: dict):
        conn = sqlite3.connect(self._CRED_DB)
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

    ### Login Process Functions ###
    '''
        function : get_user_by_id
        params: user_id
        returns : none
        descr. : connect with the app database to create and return a User object
    '''
    def get_user_by_id(self, user_id: int):
        # Connects with DB
        conn = sqlite3.connect(self._CRED_DB)
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
            return reponse_user

    '''
        function : get_details_by_username
        params: username
        returns : none
        descr. : connect with the app database to return a user's id, username, password, role, and last login
    '''
    def get_details_by_username(username: str):
        conn = sqlite3.connect(CRED_DATABASE)
        curs = conn.cursor()
        curs.execute("select * from users where username=(?);", [username])
        user_details = curs.fetchone()
        conn.commit()
        conn.close()
        return(user_details)

    '''
        function : update_last_login_by_username
        params: username
        returns : none
        descr. : connect with the app database to update a user's last login
    '''
    def update_last_login_by_username(self, username: str):
        # Connects with DB
        conn = sqlite3.connect(self._CRED_DB)
        curs = conn.cursor()
        # Updates last login with current date and time
        # YYYY/MM/DD HH:MM:SS.SSS
        new_time = date.now().strftime("%Y/%m/%d %H:%M:%S")
        cur.execute("update users set lastlogin=(?) where username=(?)", [new_time, username])
        conn.commit()
        conn.close()

    ### Administrative Functions ###
    '''
        function : set_role
        params: user_id, role
        returns : none
        descr. : connect with the app database to update user permissions / role
    '''
    def set_role(self, user_id: int, role: int):
        conn = sqlite3.connect(self._CRED_DB)
        curs = conn.cursor()
        curs.execute("update users set role=(?) where userid=(?)", [role, user_id])
        conn.commit()
        conn.close()

    '''
        function : delete_users
        params: users
        returns : none
        descr. : connect with the app database to erase a user from the application
    '''
    def delete_user(self, user_id: int):
        conn = sqlite3.connect(self._CRED_DB)
        curs = conn.cursor()
        curs.execute("delete from users where userid=(?);", [user_id])
        conn.commit()
        conn.close()
