import sqlite3
from sqlite3 import Error
import os, os.path
import random
import string

DIR = os.getcwd() + os.path.sep + "databases" + os.path.sep + "sqlite3"
CRED_FILE = DIR + os.path.sep + "chessEDU_credentials.db"
JSON_FILE = DIR + os.path.sep + "chessEDU_User_JSONs.db"

# Generate a 15-characer long password for the admin account
def admin_password() -> str:
    length = 15
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    random.seed = os.urandom(1024)
    password = ''.join(random.choice(chars) for i in range(length))
    return(password)

# Creates database directory if it does not already exist
def create_directory() -> bool:
    try:
        if(os.path.isdir(DIR)):
            return True
        else:
            os.makedirs(DIR)
            return True
    except Error as e:
        print(e)
        return False

# Creates database (not tables)
def create_database(FILE) -> bool:
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(FILE)
        return_value = True
    except Error as e:
        print(e)
        return_value = False
    finally:
        if conn:
            conn.close()
        return return_value

def create_user_tables() -> bool:
    conn = sqlite3.connect(CRED_FILE)
    c = conn.cursor()
    try:
        # Create user table
        c.execute("create table users(userid int primary key not null, username text not null, password text not null, role int not null, lastlogin text not null);")
        conn.commit()
        conn.close()
        return True
    except Error as e:
        conn.commit()
        conn.close()
        print(e)
        return False

def create_sqlar_table() -> bool:
    conn = sqlite3.connect(JSON_FILE)
    c = conn.cursor()
    try:
        # Create sqlar table
        # userid int primary key -- id of the user
        # name text -- name of the user's JSON file (the full pathname relative to the root of the archive)
        c.execute("create table sqlar(userid int primary key not null, name text not null);")
        conn.commit()
        conn.close()
        return True
    except Error as e:
        conn.commit()
        conn.close()
        print(e)
        return False

# Create admin account (no other users should exist, so ID is hard-coded to 1)
def create_admin() -> str:
    cred_conn = sqlite3.connect(CRED_FILE)
    cred_c = cred_conn.cursor()
    password = admin_password()
    try:
        # Create admin user : netarch_admin
        create_user_string = f'insert into users values(1, \"chessEDU_admin\", \"{password}\", 0, \"0000-00-00 00:00:00.000\")'
        cred_c.execute(create_user_string)
        cred_conn.commit()
        cred_conn.close()

        JSON_conn = sqlite3.connect(JSON_FILE)
        JSON_c = JSON_conn.cursor()
        create_file_string = f'insert into sqlar values(1, \"NO ADMIN FILE\")'
        JSON_c.execute(create_file_string)
        JSON_conn.commit()
        JSON_conn.close()
        return(password)
    except Error as e:
        print(e)
        return(None)

def deploy_db():
    if create_directory():
        if create_database(JSON_FILE) and create_database(CRED_FILE):
            if create_user_tables() and create_sqlar_table():
                print("Successfully created user sqlar and credential databases")
                password = create_admin()
                if (password is not None):
                    print(f"Successfully created admin\n\t Username: \"chessEDU_admin\"\n\tPassword: \"{password}\"")
                else:
                    print("Unable to create admin user")
            else:
                print("Unable to create credential and sqlar database tables")
        else:
            print("Unable to create user sqlar and credential databases")
    else:
        print("Unable to create database directory")

if __name__ == "__main__":
    deploy_db()
