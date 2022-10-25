from flask_login import UserMixin
import os
from datetime import datetime
### User Management ###
# User class : Stores data on current session's user
class User(UserMixin):
    '''
        Method : constructor (__init__)
        Param : self, id(int), username(str), password(str), details(dict), roles(dict)
        Return : none
        Descr. : sets self attributes
    '''
    def __init__(self, id, username, password, role, lastlogin, courses):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False
        self.role = role
        # YYYY-MM-DD HH:MM:SS.SSS
        self.lastlogin = lastlogin
        #[<Course ID> :: Int]
        self.courses = courses

    '''
        Method : is_active
        Param : self
        Return : Bool self.is_active()
        Descr. : Required function by flask-login
    '''
    def is_active(self):
        return self.is_active()

    '''
        Method : is_anonymous
        Param : self
        Return : False
        Descr. : Required function by flask-login, should always be false for this application
    '''
    def is_anonymous(self):
        return False

    '''
        Method : is_authenticated
        Param : self
        Return : Bool
        Descr. : Required function by flask login, used in @login_required routes
    '''
    def is_authenticated(self):
        return self.authenticated

    '''
        Method : is_active
        Param : self
        Return : True
        Descr. : required function by flask-login, all users should be active (session timeout kills all user information)
    '''
    def is_active(self):
        return True

    '''
        Method : get_details
        Param : self
        Return : self.roles dictionary
        Descr. : To be used in checking user details such as name and last login
    '''
    def get_courses(self):
        return self.courses

    '''
        Method : get_roles
        Param : self
        Return : self.roles dictionary
        Descr. : To be used in checking a user's access rights
    '''
    def get_role(self):
        return self.role

    '''
        Method : get_id
        Param : self
        Return : self.id int
        Descr. : Used in logging users in (only the encrypted user id is stored in the session)
    '''
    def get_id(self):
        return self.id
