import sqlite3 as sql

from core.general.file_locations import rel_loc
from core.log.console_log import c_log, TColors as Color


def delete_user(f_name, l_name, uid, locker):
    # connection to datatabase
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # delete user
    cursor_accs.execute("DELETE FROM users WHERE first_name = (?) AND last_name = (?) AND uid = (?) AND locker = (?)",
                        (f_name, l_name, uid, locker))

    # save and close connection
    conn_accs.commit()
    conn_accs.close()

    c_log(Color.OKGREEN, "Deleted " + f_name + " " + l_name + " from database successfully")
