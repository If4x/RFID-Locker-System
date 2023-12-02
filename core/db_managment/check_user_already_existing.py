import sqlite3 as sql
from core.general.file_locations import rel_loc
from core.log.console_log import c_log, TColors as Color


def check_name(f_name, l_name):
    # connection to database
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # select every entry with this name
    cursor_accs.execute("SELECT * FROM users WHERE first_name = (?) AND last_name = (?)",
                        (f_name, l_name))
    result = cursor_accs.fetchone()

    # if no entry found
    if result is None:
        c_log(Color.OKCYAN, "No user found with this name")
        return True
    else:
        c_log(Color.WARNING, "Found an user with this name")
        return False


def check_uid(uid):
    # connection to database
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # select every entry with this uid
    cursor_accs.execute("SELECT * FROM users WHERE uid = (?)",
                        (uid, ))
    result = cursor_accs.fetchone()

    # if no entry found
    if result is None:
        c_log(Color.OKCYAN, "No user found with this uid")
        return True
    else:
        c_log(Color.WARNING, "Found an user with this uid")
        return False


def check_locker(locker):
    # connection to database
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # select every entry with this locker
    cursor_accs.execute("SELECT * FROM users WHERE locker = (?)",
                        (locker, ))
    result = cursor_accs.fetchone()

    # if no entry found
    if result is None:
        c_log(Color.OKCYAN, "No user found with this locker")
        return True
    else:
        c_log(Color.WARNING, "Found an user with this locker")
        return False
