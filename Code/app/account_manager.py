import os
import sqlite3
import json
from pathlib import Path
from datetime import date
import os, os.path

class AccountManager():
    def __init__(self):
        self._CRED_DB = str(Path(f"{os.getcwd()}").parents[0])+os.path.sep+"deployment"+os.path.sep+"databases"+os.path.sep+"sqlite3"+os.path.sep+"chessEDU_credentials.db"
        self._JSON_DB = str(Path(f"{os.getcwd()}").parents[0])+os.path.sep+"deployment"+os.path.sep+"databases"+os.path.sep+"sqlite3"+os.path.sep+"chessEDU_User_JSONs.db"

    ### Sign Up Process Functions ###
    '''
        function : create_new_user
        params: user - Dict: {"new_username": str, "new_password": str, "role", 0/1}
        returns : none
        descr. : connect with the app database to create a new user
    '''
    def create_new_user(self, user: dict):
        # Add the user's credentials to the credentials database
        new_id = 0
        cred_conn = sqlite3.connect(self._CRED_DB)
        cred_curs = cred_conn.cursor()
        cred_curs.execute("select * from users where username=(?);", [user["new_username"]])
        existinguser = cred_curs.fetchone()
        if existinguser == None:
            cred_curs.execute("select max(userid) from users;")
            new_id = 1 + cred_curs.fetchone()[0]

            JSON_conn = sqlite3.connect(self._JSON_DB)
            JSON_curs = JSON_conn.cursor()
            JSON_curs.execute("select * from sqlar where userid=(?);", [new_id])
            existingfile = JSON_curs.fetchone()
            if existingfile == None:
                # Create credentials entry for the user
                # sqlite execute function takes a list as a parameter, so put new user values in a list
                new_user = []
                # New id
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
                cred_curs.execute("insert into users values ((?), (?), (?), (?), (?));", new_user)
                cred_conn.commit()
                cred_conn.close()

                # Create a JSON file for the user and track store its location in the database
                # sqlite execute function takes a list as a parameter, so put new file values in a list
                new_file = []
                # New id
                new_file.append(new_id)
                # New filepath
                FILEPATH = os.getcwd() + os.path.sep + "user_JSONS" + os.path.sep + user["new_username"]
                print(FILEPATH)
                new_file.append(FILEPATH)
                # Add file to sqlar table
                JSON_curs.execute("insert into sqlar values ((?), (?));", new_file)
                JSON_conn.commit()
                JSON_conn.close()

                try:
                    new_JSON = open(FILEPATH, "x")
                    user_data = {
                        "username": user["new_username"],
                        "id": new_id,
                        "progress": {}
                    }
                    json_string = json.dumps(user_data)
                    new_JSON.write(json_string)
                    new_JSON.close()
                except:
                    raise
            else:
                cred_conn.close()
                JSON_conn.close()
        else:
            conn.close()
            raise

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
            return response_user

    '''
        function : get_details_by_username
        params: username
        returns : none
        descr. : connect with the app database to return a user's id, username, password, role, and last login
    '''
    def get_details_by_username(self, username: str):
        conn = sqlite3.connect(self._CRED_DB)
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
