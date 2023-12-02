import sqlite3 as sql
from core.general.file_locations import rel_loc
from core.log.console_log import c_log, TColors as Color


def new_user(f_name, l_name, uid, locker):
    # connection to database
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # insert new user into database
    cursor_accs.execute("INSERT INTO users VALUES (?,?,?,?)", (f_name, l_name, uid, locker))

    # save and close connection
    conn_accs.commit()
    conn_accs.close()

    c_log(Color.OKCYAN, "User " + f_name + " " + l_name + " (UID: " + uid + " | locker: " + locker + ") has been added to the database.")
