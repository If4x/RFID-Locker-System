class User:
    user_f_name = None
    user_l_name = None
    user_locker = None
    user_uid = None

    def __init__(self, f_name, l_name, locker, uid):
        self.user_f_name = f_name
        self.user_l_name = l_name
        self.user_locker = locker
        self.user_uid = uid


class Admin:
    admin_username = None
    admin_psw_entered = None

    def __init__(self, username, psw_entered):
        self.admin_username = username
        self.admin_psw_entered = psw_entered
