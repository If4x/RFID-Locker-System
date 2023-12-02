import sqlite3 as sql
from core.general.hash import hashing
from core.general.file_locations import rel_loc
from core.log.console_log import c_log, TColors as Color


def check_password(username, password_entered):

    # connection to database
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # get password out of database
    cursor_accs.execute("SELECT password FROM admins WHERE username = (?)", (username,))
    items = cursor_accs.fetchone()

    # user exists?
    if items is not None:
        password_db = items[0]
        print("psw_db", password_db)
    else:
        password_db = None

    # hash entered password
    password_entered_hashed = hashing(password_entered)

    # check if user exists. if not return False
    if password_db is None:
        c_log(Color.FAIL, "User does not exist")
        return False

    # check if passwords are the same and return corresponding value
    elif password_entered_hashed == password_db:
        c_log(Color.OKGREEN, "password is correct")
        return True
    else:
        c_log(Color.FAIL, "Wrong password")
        return False
