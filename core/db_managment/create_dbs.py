import sqlite3 as sql
from core.general.file_locations import rel_loc


def create():
    # db users
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()
    # users
    cursor_accs.execute("""CREATE TABLE IF NOT EXISTS users(
        first_name TEXT,
        last_name TEXT,
        uid TEXT,
        locker INTEGER)""")
    # admins
    cursor_accs.execute("""CREATE TABLE IF NOT EXISTS admins(
        username TEXT,
        password TEXT)""")
    conn_accs.commit()
    conn_accs.close()

    # db log

    conn_log = sql.connect(rel_loc.db_log)
    cursor_log = conn_log.cursor()
    # log for lockers
    cursor_log.execute("""CREATE TABLE IF NOT EXISTS log_lockers(
        f_name TEXT,
        l_name TEXT,
        locker INTEGER,
        time TEXT)""")
    # log for admin logins
    cursor_log.execute("""CREATE TABLE IF NOT EXISTS log_admins(
        username TEXT,
        time TEXT)""")
    conn_log.commit()
    conn_log.close()
