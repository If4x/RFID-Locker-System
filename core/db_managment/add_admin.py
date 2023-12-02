import sqlite3 as sql
from core.general.hash import hashing
from core.general.file_locations import rel_loc
from core.log.console_log import c_log, TColors as Color


def add_admin(username, password):
    # connection to db
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # hash password
    password_hashed = hashing(password)

    # insert into database
    cursor_accs.execute("INSERT INTO admins VALUES(?,?)", (username, password_hashed))

    # save and close connection
    conn_accs.commit()
    conn_accs.close()

    c_log(Color.OKGREEN, "Admin has been added to database")
