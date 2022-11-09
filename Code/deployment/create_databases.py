import sqlite3
from sqlite3 import Error
import os, os.path
import random
import string

DIR = os.getcwd() + os.path.sep + "databases" + os.path.sep + "sqlite3"
MOD_FILE = DIR + os.path.sep + "chessEDU_modules.db"
CRED_FILE = DIR + os.path.sep + "chessEDU_credentials.db"

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
        return True
    except Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.commit()
            conn.close()

def create_sqlar_table() -> bool:
    conn = sqlite3.connect(MOD_FILE)
    c = conn.cursor()
    try:
        # Create sqlar table
        # name text primary key -- name of the file (the full pathname relative to the root of the archive)
        # mtime int             -- last modification time
        # sz int                -- original file zie
        # data blob             -- compressed content
        c.execute("create table sqlar(name text primary key not null, mode int not null, mtime int not null, sz int not null, data blob not null);")
        return True
    except Error as e:
        print(e)
        return False
    finally:
        if conn:
            conn.commit()
            conn.close()

# Create admin account (no other users should exist, so ID is hard-coded to 1)
def create_admin() -> str:
    conn = sqlite3.connect(CRED_FILE)
    c = conn.cursor()
    password = admin_password()
    try:
        # Create admin user : netarch_admin
        create_user_string = f'insert into users values(1, \"chessEDU_admin\", \"{password}\", 0, \"0000-00-00 00:00:00.000\")'
        c.execute(create_user_string)
        conn.commit()
        return(password)
    except Error as e:
        print(e)
        return(None)

def deploy_db():
    if create_directory():
        if create_database(MOD_FILE) and create_database(CRED_FILE):
            if create_user_tables():
                print("Successfully created module sqlar and credential databases")
                password = create_admin()
                if (password is not None):
                    print(f"Successfully created admin\n\t Username: \"chessEDU_admin\"\n\tPassword: \"{password}\"")
                    if create_sqlar_table():
                        print("Successfully created module sqlar tables")
                    else:
                        print("Unable to create sqlar database and tables")
                else:
                    print("Unable to create admin user")
            else:
                print("Unable to create credential database tables")
        else:
            print("Unable to create module sqlar and credential databases")
    else:
        print("Unable to create database directory")

if __name__ == "__main__":
    deploy_db()
