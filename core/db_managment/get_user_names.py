from core.general.file_locations import rel_loc
import sqlite3 as sql


def get():
    # connection to database
    conn_accs = sql.connect(rel_loc.db_log)
    cursor_accs = conn_accs.cursor()

    # select every first and last name of any user and write to list
    cursor_accs.execute("SELECT f_name, l_name FROM log_lockers")
    names_double = cursor_accs.fetchall()

    # write names only once to
    names_no_double = []
    for name in names_double:
        if [name[1], name[0]] in names_no_double:
            pass
        else:
            # write to names_no_double format: [l_name, f_name]
            names_no_double.append([name[1], name[0]])

    names_sorted = sorted(names_no_double)

    return names_sorted
