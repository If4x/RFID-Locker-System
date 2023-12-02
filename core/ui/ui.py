import tkinter.messagebox
from tkinter import *
from tkinter import ttk

# own packages

from core.db_managment.login_admin import check_password
from core.ui.pop_up_info import info
from core.log.db_log import log_admin
from core.db_managment.search_user import *
from core.db_managment.change_user import change_user
from core.db_managment.new_user import new_user
from core.db_managment.add_admin import add_admin
from core.db_managment.delete_user import delete_user as delete_user_from_db
from core.log.console_log import c_log, TColors as Color
from core.general.file_locations import rel_loc
from core.db_managment import get_user_names
from core.db_managment import get_log
from core.db_managment import check_user_already_existing as check_us_ex


class UI:

    def __init__(self):
        # create root
        self.root = Tk()
        self.root.iconbitmap(rel_loc.icon)
        self.root.withdraw()

        # create TopLevels (= Windows)
        self.login_frame = Toplevel(self.root)
        self.main_frame = Toplevel(self.root)
        self.setup_frame = Toplevel(self.root)
        self.edit_frame = Toplevel(self.root)

        # hide all Toplevel
        self.main_frame.withdraw()
        self.login_frame.withdraw()
        self.setup_frame.withdraw()
        self.edit_frame.withdraw()

        # change protocol to close all windows if one is closed
        self.root.protocol("WM_DELETE_WINDOW", self.quit_all_windows)
        self.login_frame.protocol("WM_DELETE_WINDOW", self.quit_all_windows)
        self.main_frame.protocol("WM_DELETE_WINDOW", self.quit_all_windows)
        self.setup_frame.protocol("WM_DELETE_WINDOW", self.quit_all_windows)
        self.edit_frame.protocol("WM_DELETE_WINDOW", self.quit_all_windows)

        # VARIABLE SETUP
        self.setup_variables()

        # LAYOUT
        # login
        self.setup_login_frame()
        # mainframe
        self.setup_main_frame()
        # setup frame
        self.setup_setup_frame()
        # edit user frame
        self.setup_edit_user_frame()

    def setup_variables(self):
        # general
        self.icon = rel_loc.icon

        # login
        self.login_username = StringVar()
        self.login_password = StringVar()

        # search user
        self.search_first_name = StringVar()
        self.search_last_name = StringVar()
        self.search_uid = StringVar()
        self.search_locker = StringVar()
        self.result = None

        # result search
        self.search_result_first_name = StringVar()
        self.search_result_last_name = StringVar()
        self.search_result_full_name = StringVar()
        self.search_result_uid = StringVar()
        self.search_result_locker = StringVar()

        # edit user
        self.edit_f_name = StringVar()
        self.edit_l_name = StringVar()
        self.edit_uid = StringVar()
        self.edit_locker = StringVar()

        # add user
        self.new_user_f_name = StringVar()
        self.new_user_l_name = StringVar()
        self.new_user_uid = StringVar()
        self.new_user_locker = StringVar()

        # setup
        self.setup_username = StringVar()
        self.setup_password1 = StringVar()
        self.setup_password2 = StringVar()

        # add admin
        self.new_admin_username = StringVar()
        self.new_admin_password1 = StringVar()
        self.new_admin_password2 = StringVar()
        self.new_admin_password_auth = StringVar()

    def quit_all_windows(self):

        c_log(Color.FAIL + Color.BOLD, '\n\nQUITING UI\n\n')
        self.root.quit()
        self.root.destroy()

    def start_ui(self):
        self.root.mainloop()

    def stop_ui(self):
        self.quit_all_windows()

    def show_setup(self):
        self.setup_frame.update()
        self.setup_frame.deiconify()

    def hide_setup(self):
        self.setup_frame.withdraw()

    def show_login(self):
        # hide mainframe and show login
        self.main_frame.withdraw()
        self.login_frame.update()
        self.login_frame.deiconify()

        # clear all inputs
        self.login_username.set("")
        self.login_password.set("")

    def show_mainframe(self):
        # hide login and show mainframe
        self.login_frame.withdraw()
        self.main_frame.update()
        self.main_frame.deiconify()

    def setup_login_frame(self):
        # Toplevel setup
        self.login_frame.title("Login")
        self.login_frame.iconbitmap(self.icon)
        self.login_frame.resizable(False, False)

        # grid setup
        self.login_frame.columnconfigure(0, weight=1)
        self.login_frame.columnconfigure(1, weight=3)

        # entry username
        ttk.Label(self.login_frame, text="Username:")\
            .grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.login_frame, textvariable=self.login_username, justify="left")\
            .grid(row=0, column=1, padx=5, pady=5)

        # entry password
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.login_frame, textvariable=self.login_password, show="*", justify="left")\
            .grid(row=1, column=1, padx=5, pady=5)

        # button login
        ttk.Button(self.login_frame, text="Log in", command=self.login)\
            .grid(row=2, column=0, padx=5, pady=5, sticky=E)

    def setup_main_frame(self):
        def view_search_user():
            # hide other frames
            frame_log.pack_forget()
            frame_add_admin.pack_forget()
            frame_add_user.pack_forget()
            # show search frame
            frame_search.pack()

        def view_add_user():
            # hide other frames
            frame_log.pack_forget()
            frame_search.pack_forget()
            frame_add_admin.pack_forget()
            # show add_user frame
            frame_add_user.pack()

        def view_add_admin():
            # hide other frames
            frame_log.pack_forget()
            frame_search.pack_forget()
            frame_add_user.pack_forget()
            # show add_admin frame
            frame_add_admin.pack()

        def view_log():
            # hide other frames
            frame_search.pack_forget()
            frame_add_admin.pack_forget()
            frame_add_user.pack_forget()
            # show view_log frame
            frame_log.pack()

        def change_mode():
            chosen_mode = current_mode.get()
            # search with name
            if chosen_mode == modes[0]:
                # hide other frames
                frame_search_uid.grid_forget()
                frame_search_locker.grid_forget()
                # show name frame
                frame_search_name.grid(row=2, column=0, columnspan=3)

            # search with UID
            elif chosen_mode == modes[1]:
                # hide other frames
                frame_search_name.grid_forget()
                frame_search_locker.grid_forget()
                # show name frame
                frame_search_uid.grid(row=2, column=0, columnspan=3)

            # search with locker
            elif chosen_mode == modes[2]:
                # hide other frames
                frame_search_uid.grid_forget()
                frame_search_name.grid_forget()
                # show name frame
                frame_search_locker.grid(row=2, column=0, columnspan=3)

            # invalid mode
            else:
                c_log(Color.FAIL, "Error by changing mode: invalid mode")

        def search_user_in_db():

            # decide with which value to search
            # name
            if current_mode.get() == modes[0]:
                self.result = search_name(self.search_first_name.get(), self.search_last_name.get())

            # uid
            elif current_mode.get() == modes[1]:
                self.result = search_uid(self.search_uid.get())

            # locker
            elif current_mode.get() == modes[2]:
                self.result = search_locker(int(self.search_locker.get()))

            # show results
            try:
                # write search results to result frame
                self.search_result_first_name.set(self.result[0])
                self.search_result_last_name.set(self.result[1])
                self.search_result_full_name.set(self.result[0] + " " + self.result[1])
                self.search_result_uid.set(self.result[2])
                self.search_result_locker.set(self.result[3])
                # write results to other search options
                self.search_first_name.set(self.search_result_first_name.get())
                self.search_last_name.set(self.search_result_last_name.get())
                self.search_uid.set(self.search_result_uid.get())
                self.search_locker.set(self.search_result_locker.get())

                # show results
                frame_search_result.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

            except TypeError:
                info("No User found")
                # clear search results
                self.search_result_full_name.set("")
                self.search_result_first_name.set("")
                self.search_result_last_name.set("")
                self.search_result_uid.set("")
                self.search_result_locker.set("")

        def edit_user():
            if self.result is not None:
                # show edit frame and hide mainframe
                self.main_frame.withdraw()
                self.edit_frame.update()
                self.edit_frame.deiconify()

                # write search results into entrys so admin is able to change the information
                self.edit_f_name.set(self.result[0])
                self.edit_l_name.set(self.result[1])
                self.edit_uid.set(self.result[2])
                self.edit_locker.set(self.result[3])

            else:
                info("You first have to search for an user before you're able to edit it's informations.")

        def delete_user():
            # check if user has been searched
            if self.result is not None:
                # create pop up to ask admin if user really should be deleted
                question = tkinter.messagebox.askquestion("Delete user",
                                                          "Are you sure to delete this user?")
                if question == "yes":
                    # delete user from database
                    delete_user_from_db(self.search_result_first_name.get(), self.search_result_last_name.get(), self.search_result_uid.get(), self.search_result_locker.get())
                    # clear all search values
                    self.search_first_name.set("")
                    self.search_last_name.set("")
                    self.search_uid.set("")
                    self.search_locker.set("")
                    self.search_result_full_name.set("")
                    self.search_result_first_name.set("")
                    self.search_result_last_name.set("")
                    self.search_result_uid.set("")
                    self.search_result_locker.set("")
                else:
                    info("User hasn't been deleted.")
            else:
                info("You first have to search for an user before you're able to delete it.")

        def add_user():
            # create pop up to ask admin if user really should be added
            question = tkinter.messagebox.askquestion("Add user",
                                                      "Are you sure to want to add user?")
            if question == "yes":
                # check if an user with this name ist already existing
                if check_us_ex.check_name(self.new_user_f_name.get(), self.new_user_l_name.get()):
                    # check if an user with this uid is already existing
                    if check_us_ex.check_uid(self.new_user_uid.get()):
                        # check if an user with this locker is already existing
                        if check_us_ex.check_locker(self.new_user_locker.get()):
                            # add user
                            new_user(self.new_user_f_name.get(), self.new_user_l_name.get(),
                                     self.new_user_uid.get(), self.new_user_locker.get())
                            # reset inputs
                            self.new_user_f_name.set("")
                            self.new_user_l_name.set("")
                            self.new_user_uid.set("")
                            self.new_user_locker.set("")

                        else:
                            info("An user with this locker is already existing")
                    else:
                        info("An user with this UID is already existing")
                else:
                    info("An user with this name ist already existing")
            else:
                info("User hasn't been added.")

        def add_admin_to_db():
            # check if an username and passwords for the new admin was entered and if the password do match
            # no username entered
            if self.new_admin_username.get() == "":
                info("Please enter username for new admin.")
            # at least one password is missing
            elif self.new_admin_password1.get() == "" or self.new_admin_password2.get() == "":
                info("Please enter password for new admin.")
            # passwords do not match
            elif self.new_admin_password1.get() != self.new_admin_password2.get():
                info("Passwords do not match")
            # entered information for new admin is valid
            else:
                # ask current admin if new admin really should be added
                question = tkinter.messagebox.askquestion("Add admin",
                                                          "Are you sure to add admin with this login information?")
                if question == "yes":
                    # check if authentication of current admin which is logged in is valid
                    auth = check_password(self.login_username.get(), self.new_admin_password_auth.get())
                    if auth:
                        # add admin to database
                        add_admin(self.new_admin_username.get(), self.new_admin_password1.get())

                        # clear inputs
                        self.new_admin_username.set("")
                        self.new_admin_password1.set("")
                        self.new_admin_password2.set("")
                        self.new_admin_password_auth.set("")

                        info("Admin has been added.")

                    else:
                        info("Your own password, which is needed for authentication is wrong. Please try again.")
                else:
                    info("Admin hasn't been added.")

        def show_log():
            # display the log
            def display_log_for_user(f_name, l_name):
                # clear lists
                listbox_locker.delete(0, END)
                listbox_time.delete(0, END)

                # labeling of lists
                ttk.Label(frame_log, text="locker")\
                    .grid(row=3, column=0)
                ttk.Label(frame_log, text="time") \
                    .grid(row=3, column=1)

                # show listboxes
                listbox_locker.grid(row=4, column=0, pady=5, sticky=E)
                listbox_time.grid(row=4, column=1, pady=5, sticky=W)
                scrollbar.grid(row=4, column=2, sticky= N+S)

                # insert new data into listboxes
                items = get_log.get(f_name, l_name)
                i_max = len(items)
                for i in range(0, i_max):
                    listbox_locker.insert(i, items[i_max - 1 - i][0])
                    listbox_time.insert(i, items[i_max - 1 - i][1])

            # check if an user was selected
            if combo_users.get() == "Select an user":
                info("Please select an user")
            else:
                name = [combo_users.get().split()[1], combo_users.get().split()[0]]
                c_log(Color.OKCYAN, "Searching log for " + name[0] + " " + name[1])

                display_log_for_user(name[0], name[1])

        self.main_frame.title("Admin")
        self.main_frame.iconbitmap(self.icon)
        self.main_frame.resizable(True, True)
        # setup minimal size so menu is always readable
        self.main_frame.minsize(350, 0)

        # variable to proof if an user was found and save his data

        # create different frames for tasks
        frame_search = Frame(self.main_frame)
        frame_log = Frame(self.main_frame)
        frame_add_admin = Frame(self.main_frame)
        frame_add_user = Frame(self.main_frame)
        # create sub-frames for different searching methods in search user
        frame_search_name = Frame(frame_search)
        frame_search_uid = Frame(frame_search)
        frame_search_locker = Frame(frame_search)
        frame_search_result = Frame(frame_search)

        # menu to decide what admin wants to do
        menu = Menu(self.main_frame)
        menu.add_command(label="Search", command=view_search_user)
        menu.add_command(label="Add User", command=view_add_user)
        menu.add_command(label="Log", command=view_log)
        menu.add_command(label="Add Admin", command=view_add_admin)

        # add menu to main_frame
        self.main_frame.config(menu=menu)


        # SETUP FRAMES

        # SEARCH

        # variables
        current_mode = StringVar()
        modes = ["Name", "UID", "Locker"]

        # description
        ttk.Label(frame_search, text="Pick with which value you want to search for an user.")\
            .grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        # options to decide with what you want to search
        ttk.Radiobutton(frame_search, text=modes[0], variable=current_mode, value=modes[0], command=change_mode)\
            .grid(row=1, column=0, padx=5, pady=5)
        ttk.Radiobutton(frame_search, text=modes[1], variable=current_mode, value=modes[1], command=change_mode)\
            .grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(frame_search, text=modes[2], variable=current_mode, value=modes[2], command=change_mode)\
            .grid(row=1, column=2, padx=5, pady=5)

        # for loading the mainframe, show search the first time it's loaded
        view_search_user()

        # search button
        ttk.Button(frame_search, text="Search", command=search_user_in_db)\
            .grid(row=10, column=0, padx=5, pady=5)

        # edit button
        ttk.Button(frame_search, text="Edit", command=edit_user)\
            .grid(row=10, column=1, padx=5, pady=5)

        # delete button
        ttk.Button(frame_search, text="Delete", command=delete_user)\
            .grid(row=10, column=2, padx=5, pady=5)

        # logout button
        ttk.Button(self.main_frame, text="Log out", command=self.show_login)\
            .pack(side=BOTTOM, anchor="e", padx=10, pady=10)

        # SETUP SUB-FRAMES OF SEARCH USER
        # search with name
        ttk.Label(frame_search_name, text="First name")\
            .grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame_search_name, text="Last name")\
            .grid(row=1, column=0, padx=5, pady=5)

        ttk.Entry(frame_search_name, textvariable=self.search_first_name)\
            .grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(frame_search_name, textvariable=self.search_last_name)\
            .grid(row=1, column=2, padx=5, pady=5)

        # search with uid
        ttk.Label(frame_search_uid, text="UID")\
            .grid(row=0, column=0, padx=5, pady=5)

        ttk.Entry(frame_search_uid, textvariable=self.search_uid)\
            .grid(row=0, column=1, padx=5, pady=5)

        # search with locker
        ttk.Label(frame_search_locker, text="Locker")\
            .grid(row=0, column=0, padx=5, pady=5)

        ttk.Entry(frame_search_locker, textvariable=self.search_locker)\
            .grid(row=0, column=1, padx=5, pady=5)

        # search result
        # labeling
        ttk.Label(frame_search_result, text="Name")\
            .grid(row=0, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_search_result, text="UID")\
            .grid(row=1, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_search_result, text="Locker")\
            .grid(row=2, column=0, padx=5, pady=0, sticky=E)
        # results
        ttk.Label(frame_search_result, textvariable=self.search_result_full_name)\
            .grid(row=0, column=1, padx=5, pady=0, sticky=W)
        ttk.Label(frame_search_result, textvariable=self.search_result_uid)\
            .grid(row=1, column=1, padx=5, pady=0, sticky=W)
        ttk.Label(frame_search_result, textvariable=self.search_result_locker)\
            .grid(row=2, column=1, padx=5, pady=0, sticky=W)


        # ADD USER

        # description
        ttk.Label(frame_add_user, text="To add an user, enter the following information")\
            .grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        # labeling
        ttk.Label(frame_add_user, text="First name")\
            .grid(row=1, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_add_user, text="Last name")\
            .grid(row=2, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_add_user, text="UID")\
            .grid(row=3, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_add_user, text="Locker")\
            .grid(row=4, column=0, padx=5, pady=0, sticky=E)
        # entrys
        ttk.Entry(frame_add_user, textvariable=self.new_user_f_name)\
            .grid(row=1, column=1, padx=5, pady=5)
        ttk.Entry(frame_add_user, textvariable=self.new_user_l_name)\
            .grid(row=2, column=1, padx=5, pady=5)
        ttk.Entry(frame_add_user, textvariable=self.new_user_uid)\
            .grid(row=3, column=1, padx=5, pady=5)
        ttk.Entry(frame_add_user, textvariable=self.new_user_locker)\
            .grid(row=4, column=1, padx=5, pady=5)
        # add button
        ttk.Button(frame_add_user, text="Add user", command=add_user)\
            .grid(row=5, column=0, columnspan=2, padx=5, pady=5)


        # ADD ADMIN

        # description
        ttk.Label(frame_add_admin, text="To add an admin, enter the following information.") \
            .grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ttk.Label(frame_add_admin, text="You will need to authenticate this process with your password.") \
            .grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # labeling
        ttk.Label(frame_add_admin, text="Username") \
            .grid(row=2, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_add_admin, text="Password") \
            .grid(row=3, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_add_admin, text="Repeat password") \
            .grid(row=4, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(frame_add_admin, text="password current admin") \
            .grid(row=5, column=0, padx=5, pady=0, sticky=E)
        # entrys
        ttk.Entry(frame_add_admin, textvariable=self.new_admin_username) \
            .grid(row=2, column=1, padx=5, pady=5)
        ttk.Entry(frame_add_admin, textvariable=self.new_admin_password1, show="*") \
            .grid(row=3, column=1, padx=5, pady=5)
        ttk.Entry(frame_add_admin, textvariable=self.new_admin_password2, show="*") \
            .grid(row=4, column=1, padx=5, pady=5)
        ttk.Entry(frame_add_admin, textvariable=self.new_admin_password_auth, show="*") \
            .grid(row=5, column=1, padx=5, pady=5)

        # add button
        ttk.Button(frame_add_admin, text="Add admin", command = add_admin_to_db)\
            .grid(row=6, column=0, columnspan=2, padx=5, pady=5)


        # LOG
        # description
        ttk.Label(frame_log, text="Please select the user from whom you want to see the log.") \
            .grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        ttk.Label(frame_log, text="They are sorted alphabetically by their last name.") \
            .grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # combobox with usernames (sorted alphabetically)
        user_names = get_user_names.get()
        combo_users = ttk.Combobox(frame_log, values=user_names)
        combo_users.set("Select an user")
        combo_users.grid(row=2, column=0, padx=5, pady=5)
        # show log for user button
        ttk.Button(frame_log, text="Show log", command=show_log)\
            .grid(row=2, column=1, padx=5, pady=5)
        # listboxes
        listbox_locker = Listbox(frame_log)
        listbox_time = Listbox(frame_log)
        # scollbar for listboxes
        scrollbar = ttk.Scrollbar(frame_log)
        # bind scollbar to listboxes

        def scroll(*args):
            listbox_time.yview(*args)
            listbox_locker.yview(*args)

        listbox_time.config(yscrollcommand=scrollbar.set,)
        listbox_locker.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=scroll)

    def setup_edit_user_frame(self):
        def edit_user_information():

            # create pop up to ask admin if information really should be changed
            question = tkinter.messagebox.askquestion("Save changes",
                                                      "Are you sure to want to save changes to user?"
                                                      "\nOld information will be overwritten!")
            if question == "yes":

                if self.result is not None:
                    change_name = False
                    change_uid = False
                    change_locker = False

                    # check if name was changed
                    if self.search_result_first_name.get() != self.edit_f_name.get() or self.search_result_last_name.get() != self.edit_l_name.get():
                        change_name = True
                    else:
                        pass

                    # check if uid was changed
                    if self.search_result_uid.get() != self.edit_uid.get():
                        change_uid = True
                    else:
                        pass

                    # check if locker was changed
                    if self.search_result_locker.get() != self.edit_locker.get():
                        change_locker = True
                    else:
                        pass

                    # decide what to check if it already exists in database
                    accept = True
                    f_name = self.edit_f_name.get()
                    l_name = self.edit_l_name.get()
                    uid = self.edit_uid.get()
                    locker = self.edit_locker.get()

                    # if name was changed
                    if change_name:
                        if change_uid:
                            if change_locker:
                                # if username, uid, locker was changed
                                # check
                                if check_us_ex.check_name(f_name, l_name) and check_us_ex.check_locker(locker) and check_us_ex.check_uid(uid):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    if not check_us_ex.check_name(f_name, l_name):
                                        info("An user with this name is already existing")
                                    elif not check_us_ex.check_uid(uid):
                                        info("An user with this UID is already existing")
                                    elif not check_us_ex.check_locker(locker):
                                        info("An user with this locker is already existing")

                            else:
                                # if username, uid was changed
                                # check
                                if check_us_ex.check_name(f_name, l_name) and check_us_ex.check_uid(uid):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    if not check_us_ex.check_name(f_name, l_name):
                                        info("An user with this name is already existing")
                                    elif not check_us_ex.check_uid(uid):
                                        info("An user with this UID is already existing")

                        else:
                            if change_locker:
                                # if username, locker was changed
                                # check
                                if check_us_ex.check_name(f_name, l_name) and check_us_ex.check_locker(locker):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    if not check_us_ex.check_name(f_name, l_name):
                                        info("An user with this name is already existing")
                                    elif not check_us_ex.check_locker(locker):
                                        info("An user with this locker is already existing")

                            else:
                                # if username was changed
                                # check
                                if check_us_ex.check_name(f_name, l_name):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    info("An user with this username is already existing")

                    else:
                        if change_uid:
                            if change_locker:
                                # if uid, locker was changed
                                # check
                                if check_us_ex.check_uid(uid) and check_us_ex.check_locker(locker):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    if not check_us_ex.check_uid(uid):
                                        info("An user with this UID is already existing")
                                    elif not check_us_ex.check_locker(locker):
                                        info("An user with this locker is already existing")

                            else:
                                # if uid was changed
                                # check
                                if check_us_ex.check_uid(uid):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    info("An user with this UID is already existing")

                        else:
                            if change_locker:
                                # if locker was changed
                                # check
                                if check_us_ex.check_locker(locker):
                                    accept = True
                                else:
                                    accept = False

                                    # create pop up to give information which entry is already in database
                                    info("An user with this locker is already existing")

                            else:
                                # nothing was changed
                                # create pop up to give information which entry is already in database
                                info("Nothing changed")

                    # if new information for user are valid edit information and save to database
                    if accept:
                        change_user(self.result[0], self.result[1], self.result[2], self.result[3],
                                    self.edit_f_name.get(),
                                    self.edit_l_name.get(), self.edit_uid.get(), self.edit_locker.get())
                        c_log(Color.OKCYAN, "Changed user-information")

                        # write changed user information to search menu
                        self.search_first_name.set(self.edit_f_name.get())
                        self.search_last_name.set(self.edit_l_name.get())
                        self.search_uid.set(self.edit_uid.get())
                        self.search_locker.set(self.edit_locker.get())
                        # write changed user information to search result
                        self.search_result_first_name.set(self.edit_f_name.get())
                        self.search_result_last_name.set(self.edit_l_name.get())
                        self.search_result_full_name.set(self.edit_f_name.get() + " " + self.edit_l_name.get())
                        self.search_result_uid.set(self.edit_uid.get())
                        self.search_result_locker.set(self.edit_locker.get())

                        # hide edit window and show mainframe
                        self.edit_frame.withdraw()
                        self.main_frame.update()
                        self.main_frame.deiconify()

                else:
                    c_log(Color.FAIL, "Can't display user-information: No search-result")

            else:
                info("User-informations hasn't been overwritten")

        def abort():
            # hide edit window and show mainframe
            self.edit_frame.withdraw()
            self.main_frame.update()
            self.main_frame.deiconify()

        self.edit_frame.title("Edit user")
        self.edit_frame.iconbitmap(self.icon)
        self.edit_frame.resizable(False, False)

        # description
        ttk.Label(self.edit_frame, text="Edit information to change information for user")\
            .grid(row=0, column=0, columnspan=2, padx=5, pady=0)
        # labeling
        ttk.Label(self.edit_frame, text="First name")\
            .grid(row=1, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(self.edit_frame, text="Last name")\
            .grid(row=2, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(self.edit_frame, text="UID")\
            .grid(row=3, column=0, padx=5, pady=0, sticky=E)
        ttk.Label(self.edit_frame, text="Locker")\
            .grid(row=4, column=0, padx=5, pady=0, sticky=E)
        # entrys
        ttk.Entry(self.edit_frame, textvariable=self.edit_f_name)\
            .grid(row=1, column=1, padx=5, pady=5)
        ttk.Entry(self.edit_frame, textvariable=self.edit_l_name)\
            .grid(row=2, column=1, padx=5, pady=5)
        ttk.Entry(self.edit_frame, textvariable=self.edit_uid)\
            .grid(row=3, column=1, padx=5, pady=5)
        ttk.Entry(self.edit_frame, textvariable=self.edit_locker)\
            .grid(row=4, column=1, padx=5, pady=5)

        # save changes button
        ttk.Button(self.edit_frame, text="Save changes", command=edit_user_information)\
            .grid(row=5, column=0, padx=5, pady=5)
        # aboard button
        ttk.Button(self.edit_frame, text="Abort", command=abort)\
            .grid(row=5, column=1, padx=5, pady=5)

    def setup_setup_frame(self):
        self.setup_frame.title("Setup")
        self.setup_frame.iconbitmap(self.icon)
        self.setup_frame.resizable(False, False)

        def create_system():
            if self.setup_username.get() == "":
                info("Please enter username.")
            elif self.setup_password1.get() == "" or self.setup_password2.get() == "":
                info("Please enter password.")
            elif self.setup_password1.get() != self.setup_password2.get():
                info("Passwords do not match")
            else:
                # create pop up to ask if first admin really should be added
                question = tkinter.messagebox.askquestion("Create System", "Are you sure to add first admin with this "
                                                                           "login information?")
                if question == "yes":
                    add_admin(self.setup_username.get(), self.setup_password1.get())
                    info("Setup successful!")
                    self.quit_all_windows()

                else:
                    info("First Admin hasn't been added.")

        # description
        ttk.Label(self.setup_frame, text="Please enter information for first admin account")\
            .grid(row=0, column=0, columnspan=2, padx=10, pady=15)
        # labeling
        ttk.Label(self.setup_frame, text="Username")\
            .grid(row=1, column=0, sticky=E)
        ttk.Label(self.setup_frame, text="Password")\
            .grid(row=2, column=0, sticky=E)
        ttk.Label(self.setup_frame, text="Repeat password")\
            .grid(row=3, column=0, sticky=E)
        # entrys
        ttk.Entry(self.setup_frame, textvariable=self.setup_username)\
            .grid(row=1, column=1)
        ttk.Entry(self.setup_frame, textvariable=self.setup_password1, show="*")\
            .grid(row=2, column=1)
        ttk.Entry(self.setup_frame, textvariable=self.setup_password2, show="*")\
            .grid(row=3, column=1)
        # create button
        ttk.Button(self.setup_frame, text="setup", command=create_system)\
            .grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def login(self):
        if check_password(self.login_username.get(), self.login_password.get()):
            # log admin login to database
            log_admin(self.login_username.get())

            # launch mainframe
            self.show_mainframe()
        else:
            self.login_password.set("")
            info("Wrong username or password. Please try again.")
