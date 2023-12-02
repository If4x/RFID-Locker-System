# Program by Imanuel Fehse

from core.log.console_log import c_log as cl
from core.log.console_log import TColors as Color
from core.general.check_files import check as check_files
from core.db_managment import create_dbs

cl(Color.FAIL + Color.BOLD, """
    ----------------------------
    | PROGRAM BY IMANUEL FEHSE |
    ----------------------------
""")

# check if files are missing
if check_files():
    # no files are missing
    cl(Color.OKGREEN, "No files missing")
else:
    # files are missing
    cl(Color.WARNING, "Missing databases, creating new")
    create_dbs.create()
    cl(Color.OKGREEN, "successfully")
