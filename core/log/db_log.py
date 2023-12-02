import sqlite3 as sql
from core.general.get_time import date_time
from core.general.file_locations import rel_loc


def log_locker(f_name, l_name, locker):
    # create connection
    conn_log = sql.connect(rel_loc.db_log)
    cursor_log = conn_log.cursor()
    # insert log into database
    cursor_log.execute("INSERT INTO log_lockers VALUES(?,?,?,?)", (f_name, l_name, locker, date_time()))
    # commit and close connection to database
    conn_log.commit()
    conn_log.close()


def log_admin(username):
    # create connection
    conn_log = sql.connect(rel_loc.db_log)
    cursor_log = conn_log.cursor()
    # insert username and time into admin log database
    cursor_log.execute("INSERT INTO log_admins VALUES(?,?)", (username, date_time()))

    # save and close connection
    conn_log.commit()
    conn_log.close()
