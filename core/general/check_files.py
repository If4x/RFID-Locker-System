from core.general import file_locations


def check():
    try:
        open(file_locations.rel_loc.db_accounts, "r").close()
        open(file_locations.rel_loc.db_log, "r").close()
        return True
    except FileNotFoundError:
        return False
