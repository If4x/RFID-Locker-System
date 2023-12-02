import sqlite3 as sql

from core.general.file_locations import rel_loc


def change_user(old_f_name, old_l_name, old_uid, old_locker, new_f_name, new_l_name, new_uid, new_locker):
    # create connection to database
    conn_accs = sql.connect(rel_loc.db_accounts)
    cursor_accs = conn_accs.cursor()

    # search user whichs information should be changed
    cursor_accs.execute("SELECT rowid FROM users WHERE first_name = (?) AND last_name = (?) AND uid = (?) AND locker = (?)",
                        (old_f_name, old_l_name, old_uid, old_locker))
    row_id = cursor_accs.fetchone()
    row_id = row_id[0]
    print("rowid:", row_id)

    # change values
    cursor_accs.execute("UPDATE users SET first_name = (?) WHERE rowid = (?)", (new_f_name, row_id))
    cursor_accs.execute("UPDATE users SET last_name = (?) WHERE rowid = (?)", (new_l_name, row_id))
    cursor_accs.execute("UPDATE users SET uid = (?) WHERE rowid = (?)", (new_uid, row_id))
    cursor_accs.execute("UPDATE users SET locker = (?) WHERE rowid = (?)", (new_locker, row_id))

    # save and close connection
    conn_accs.commit()
    conn_accs.close()
