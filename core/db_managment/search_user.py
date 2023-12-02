import sqlite3 as sql
from core.general.file_locations import rel_loc
from core.log.console_log import c_log, TColors as Color


def search_in_db(search_with, value):
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # search with name/uid/locker
    if search_with == "name":
        c_log(Color.OKCYAN, "Searching with: name")
        cursor_accs.execute("SELECT * FROM users WHERE first_name = (?) AND last_name = (?)", (value[0], value[1]))
        items = cursor_accs.fetchone()
        print(items)
        return items

    elif search_with == "uid":
        c_log(Color.OKCYAN, "Searching with: uid")
        cursor_accs.execute("SELECT * FROM users WHERE uid = (?)", (value,))
        items = cursor_accs.fetchone()
        print(items)
        return items

    elif search_with == "locker":
        c_log(Color.OKCYAN, "Searching with: locker")
        cursor_accs.execute("SELECT * FROM users WHERE locker = (?)", (value,))
        items = cursor_accs.fetchone()
        print(items)
        return items

    else:
        c_log(Color.FAIL, "Searching with: ERROR")

    conn_accs.close()


def search_name(f_name, l_name):
    full_name = [f_name, l_name]
    result = search_in_db("name", full_name)

    return result


def search_uid(uid):
    result = search_in_db("uid", uid)
    return result


def search_locker(locker):
    result = search_in_db("locker", locker)
    return result
