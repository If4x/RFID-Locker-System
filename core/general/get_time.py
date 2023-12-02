# return current date and time
import datetime


def date_time():
    return datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S")
