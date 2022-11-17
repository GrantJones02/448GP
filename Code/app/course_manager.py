import os
import sqlite3
from pathlib import Path
from datetime import date

class CourseManager():
    def __init__(self):
        self._CRED_DB = str(Path(f"{os.getcwd()}").parents[0])+os.path.sep+"deployment"+os.path.sep+"databases"+os.path.sep+"sqlite3"+os.path.sep+"chessEDU_courses.db"

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
    def get_course_by_id(self, course_id: int):
        # Connects with DB
        conn = sqlite3.connect(self._CRED_DB)
        curs = conn.cursor()
        # Gets entire user profile based on ID
        curs.execute("select * from courses where courseid=(?);", [user_id])
        response_user = curs.fetchone()
        conn.commit()
        conn.close()
        # If either query returns no results, course does not exist
        if response_course is None:
            return None
        else:
            return response_course

    '''
        function : delete_course
        params: course_id
        returns : none
        descr. : connect with the app database to erase a course from the application
    '''
    def delete_course(self, course_id: int):
        conn = sqlite3.connect(self._CRED_DB)
        curs = conn.cursor()
        curs.execute("delete from users where userid=(?);", [user_id])
        conn.commit()
        conn.close()
