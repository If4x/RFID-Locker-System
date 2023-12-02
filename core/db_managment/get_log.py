import sqlite3 as sql
from core.general.file_locations import rel_loc


def get(f_name, l_name):
    print(f_name, type(f_name))
    print(l_name, type(l_name))
    # connection to database
    conn_log = sql.connect(rel_loc.db_log)
    cursor_log = conn_log.cursor()

    # Select every log from user
    cursor_log.execute("SELECT locker, time FROM log_lockers WHERE f_name = (?) AND l_name = (?)",
                       (f_name, l_name))
    items = cursor_log.fetchall()
    print(items)

    # save and close connection
    conn_log.commit()
    conn_log.close()
    return items
