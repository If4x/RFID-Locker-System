from core.log.console_log import c_log, TColors as Color
from core.db_managment.create_dbs import create
from core.general.check_files import check
from core.ui.ui import UI
from core.ui.pop_up_info import info
from core.general.file_locations import rel_loc

import tkinter.messagebox
import os


# create system
def setup():
    c_log(Color.OKGREEN, "Running Setup")
    create()
    c_log(Color.OKGREEN, "\nCreated Databases")

    # create UI to launch setup screen to enter first admin information
    ui = UI()

    ui.show_setup()

    ui.start_ui()

    c_log(Color.OKGREEN + Color.BOLD, "SETUP COMPLETE")


# check if system hasn't already been installed
# if not: create databases
if check():
    c_log(Color.WARNING, "System installation already has been run on this system.")

    question = tkinter.messagebox.askquestion("Create System", "System Setup already has been run on this system."
                                                               " Do you want to delete old system and install "
                                                               "a new one?")
    if question == "yes":
        # if accounts database exists
        if os.path.isfile(rel_loc.db_log):
            # delete db
            os.remove(rel_loc.db_log)
            c_log(Color.BOLD + Color.WARNING, "Deleted core/ds/log.db")

        # if log database exists
        if os.path.isfile(rel_loc.db_accounts):
            # delete db
            os.remove(rel_loc.db_accounts)
            c_log(Color.BOLD + Color.WARNING, "Deleted core/ds/accounts.db")

        # run setup
        setup()

    else:
        info("Keeping old system and closing setup.")
else:
    setup()
