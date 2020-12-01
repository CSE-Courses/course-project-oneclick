from tkinter import *
import re
from tkcalendar import Calendar
from database import loginDatabase
from database import usersDatabase
from datetime import date
from datetime import time
from PIL import Image, ImageTk
import eventscheduler
import threading


class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master)

        # page_color = '#00c6d4'
        page_color = 'DarkGoldenrod1'
        Frame.configure(self, bg=page_color)
        load = Image.open("logo.png")
        zoom = 0.5
        pixels_x, pixels_y = tuple([int(zoom * x) for x in load.size])

        render = ImageTk.PhotoImage(load.resize((pixels_x, pixels_y)))
        self.img = Label(self.master, image=render, bg='cornflowerblue')
        self.img.image = render
        self.img.place(x=410, y=50)
        self.label_email = Label(self, text='Email', bg=page_color, font='ComicSansMS 25 bold')
        self.label_password = Label(self, text='Password', bg=page_color, font='ComicSansMS 25 bold')
        self.label_create_acct = Label(self, text='Create Account', fg='blue', font='ComicSansMS', cursor='hand2',
                                       bg=page_color)
        self.label_create_acct.bind('<Button-1>', lambda e: self.create_clicked())

        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show='*')

        self.label_email.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.login_button = Button(self, text='Login', font='ComicSansMS 15 bold', fg='lime green',
                                   command=self.login_clicked)
        self.login_button.grid(columnspan=2)
        self.label_create_acct.grid(columnspan=2)
        loginDatabase.create_users_table()

        self.pack()
        self.place(x=330, y=330)

    def login_clicked(self):
        # Check database for username and password and allow/disallow access
        email = self.entry_email.get()
        password = self.entry_password.get()
        if check_login(email, password):
            self.master.destroy()
            self.master = Tk()
            self.master.title('OneClick')
            self.master.geometry('1280x720')
            self.master.configure(bg='cornflowerblue')
            app = MainWindow(self.master, email)
        print(email)
        print(password)

    def create_clicked(self):
        self.master.destroy()
        self.master = Tk()
        self.master.title('Create Account')
        self.master.geometry('1000x1000')
        page_color = '#00c6d4'
        self.master.configure(bg='DarkGoldenrod1')
        app = CreateAccount(self.master)


class UpdateInfo(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.info_frame = Frame(master, width=150, height=300, bg='DarkGoldenrod1')
        self.info_label = Label(self.info_frame, text='Password', bg=page_color, font='ComicSansMS 25 bold')
        self.info_label.pack()
        self.info_entry = Entry(self.info_frame)
        self.info_entry.pack()
        self.info_frame.pack()


class CreateAccount(Frame):
    def __init__(self, master):
        super().__init__(master)

        # page_color = '#00c6d4'
        page_color = 'DarkGoldenrod1'
        Frame.configure(self, bg=page_color)
        self.label_email = Label(self, text='Email', bg=page_color, font='ComicSansMS 25 bold')
        self.label_password = Label(self, text='Password', bg=page_color, font='ComicSansMS 25 bold')
        self.label_pass_confirm = Label(self, text='Confirm Password', bg=page_color, font='ComicSansMS 25 bold')

        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show='*')
        self.entry_pass_confirm = Entry(self, show='*')

        self.label_email.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.label_pass_confirm.grid(row=2, sticky=E)
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.entry_pass_confirm.grid(row=2, column=1)

        self.create_button = Button(self, text='Create Account', bg=page_color, fg='brown', font='ComicSansMS',
                                    command=self.create_account)
        self.create_button.grid(columnspan=2)
        self.pack()
        self.place(x=330, y=330)

    def create_account(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        pass_confirm = self.entry_pass_confirm.get()
        if check_email(email) and check_password(password) and check_confirm_pass(pass_confirm, password):
            # Confirm account has been created in database
            loginDatabase.addUser(email, password)
            self.master.destroy()
            self.master = Tk()
            self.master.title('Login')
            self.master.geometry('1000x1000')
            app = LoginWindow(self.master)
        else:
            self.entry_email.delete(0, 'end')
            self.entry_password.delete(0, 'end')
            self.entry_pass_confirm.delete(0, 'end')


class UpdateWindow(Frame):
    def __init__(self, master, email, event_name, tup, chosen):
        super().__init__(master)
        self.email = email
        self.event_name = event_name
        self.tup = tup
        self.chosen = chosen

        self.frame = Frame(master, width=240, height=720, bg='DarkGoldenrod1')
        self.frame.pack()
        self.info_entry = Entry(self.frame)
        self.info_entry.pack()
        self.submit_button = Button(self.frame, text='Submit', command=self.submit_clicked)
        self.submit_button.pack()

    def give_date(self, date_str):
        split_date = date_str.split("/")
        return date(int("20" + split_date[2]), int(split_date[0]), int(split_date[1]))

    def give_time(self,time_str):
        split_time = time_str.split(':')
        hour = int(split_time[0])
        min = int(split_time[1])
        return time(hour,min)

    def submit_clicked(self):
        new_info = self.info_entry.get()
        #print('email:' + self.email + ', event_name:' + self.event_name + ', new_info:' + new_info + ', chosen:' + self.chosen)
        if self.chosen == 'event name':
            new_chosen = 'event_name'
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[0], new_info)
        elif self.chosen == 'description':
            usersDatabase.update_user_string(self.email, self.event_name, self.chosen, self.tup[1], new_info)
        elif self.chosen == 'zoom link':
            new_chosen = 'zoom_link'
            print('zoom link chosen now executing statement')
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[2], new_info)
        elif self.chosen == 'date':
            new_date = self.give_date(new_info).strftime("%Y-%m-%d")
            new_chosen = 'event_date'
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[3], new_date)
        elif self.chosen == 'start time':
            new_time = self.give_time(new_info)
            new_chosen = 'start_time'
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[4], new_time)
        else:
            new_time = self.give_time(new_info)
            new_chosen = 'end_time'
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[5], new_time)

        self.master.destroy()












class MainWindow(Frame):
    def __init__(self, master, email):
        super().__init__(master)
        self.email = email
        self.pack()

        load = Image.open("oneclicklogo.png")
        render = ImageTk.PhotoImage(load)
        self.img = Label(self.master, image=render, bg='cornflowerblue')
        self.img.image = render
        self.img.place(x=350, y=40)

        self.frame = Frame(master, width=240, height=720, bg='lightcoral')
        self.frame.pack(side=LEFT, fill=BOTH)
        self.add_button = Button(self.frame, text='Make Appointment', command=self.create_event)
        self.event_frame = Frame(master, width=240, height=720, bg='yellow')
        self.variable = StringVar(self.event_frame)
        self.my_events_label = Label(self.event_frame, text="My Events", bg='lightblue', font='bold', padx=1, pady=1)
        # self.event_one_label = Label(self.event_frame, text="Event One", bg='lightpink', font='bold', padx=20, pady=20)
        self.event_frame.pack(side=RIGHT, fill=BOTH)

        def dynamic_delete(event_name):
            usersDatabase.delete_user_event(self.email, event_name)
            self.master.destroy()
            self.master = Tk()
            self.master.title('OneClick')
            self.master.geometry('1280x720')
            self.master.configure(bg='cornflowerblue')
            app = MainWindow(self.master, email)

        def up_event_clicked(event_name, tup):

            chosen = self.option()
            #self.master.destroy()
            self.master = Tk()
            title = 'Enter new ' + chosen
            if chosen == 'date':
                title = 'Enter new date in mm/dd/yy format'
            if chosen == 'start time':
                title = 'Enter new start time in hh:mm format'
            if chosen == 'endtime':
                title = 'Enter new end time in hh:mm format'
            self.master.title(title)
            self.master.geometry('500x500')
            self.master.configure(bg='DarkGoldenrod1')
            UpdateWindow(self.master, email, event_name, tup, chosen)




        def refresh():
            event_dict = usersDatabase.get_user_events(self.email)
            #   for widget in self.event_frame.winfo_children():
            #      widget.destroy()
            self.my_events_label.pack()
            # self.event_one_label.pack()

            for key in event_dict:
                tup = event_dict[key]
                size = len(tup)
                date = tup[2].strftime('%m %d %Y')
                str_date = date.split(' ')
                new_date = str_date[0] + '/' + str_date[1] + '/' + str_date[2]
                info = key + '\n' + 'Description:' + tup[1] + '\n' + 'Zoom Link:' + tup[
                    0] + '\n' + 'Date:' + new_date + '\n' + 'Start Time:' + str(tup[3]) + '\n' + 'End Time:' + str(
                    tup[4])
                self.pass_tuple = (key, tup[1], tup[0], tup[2], tup[3], tup[4])
                event = Label(self.event_frame, text=info, bg='lightpink', font='bold', padx=20, pady=20)
                event.pack()
                option_list = ['event name', 'zoom link', 'description', 'date', 'start time', 'end time']
                # self.variable = StringVar(self.event_frame)
                self.variable.set(option_list[0])
                self.variable.trace("w", self.option)
                self.update_options = OptionMenu(self.event_frame, self.variable, *option_list)
                self.update_options.pack()
                self.update_button = Button(self.event_frame, text='Update', bg='hot pink',
                                            command=lambda i=key: up_event_clicked(i,self.pass_tuple))
                self.update_button.pack()
                self.del_button = Button(self.event_frame, text='Delete Event', bg='hot pink',
                                         command=lambda i=key: dynamic_delete(i))
                self.del_button.pack()

        ref_func = refresh()

        self.add_button.pack()

    def option(self, *args):
        return self.variable.get()

    def create_event(self):

        self.add_button.pack_forget()
        self.calendar = Calendar(self.frame, font='Arial 14', cursor='dotbox', selectmode='day',
                                 showothermonthdays=False, showweeknumbers=False, firstweekday='sunday')
        self.label_event = Label(self.frame, text='Event Name')
        self.label_descr = Label(self.frame, text='Description')
        self.label_command = Label(self.frame, text='Application Selection')
        self.label_link = Label(self.frame, text='Zoom Link')

        self.entry_event = Entry(self.frame, width=64)
        self.entry_descr = Text(self.frame, width=48, height=5)
        self.entry_link = Entry(self.frame, width=64)

        self.calendar.pack()
        self.label_event.pack(padx=20)
        self.entry_event.pack(padx=20)
        self.label_descr.pack(padx=20)
        self.entry_descr.pack(padx=20)
        self.label_link.pack(padx=20)
        self.entry_link.pack(padx=20)

        self.start_label = Label(self.frame, text='Start Time: ')
        self.start_label.pack(side=LEFT, padx=(20, 0))
        self.start_hourstr = StringVar(self.frame, '10')
        self.start_hour = Spinbox(self.frame, from_=0, to=23, wrap=True, textvariable=self.start_hourstr, width=2,
                                  state="readonly")
        self.start_minstr = StringVar(self.frame, '30')
        self.start_minstr.trace("w", self.trace_var)
        self.start_last_value = ""
        self.start_min = Spinbox(self.frame, from_=0, to=59, wrap=True, textvariable=self.start_minstr, width=2,
                                 state="readonly")
        self.start_hour.pack(side=LEFT)
        self.start_min.pack(side=LEFT, padx=(0, 20))

        self.end_label = Label(self.frame, text='End Time: ')
        self.end_label.pack(side=LEFT)
        self.end_hourstr = StringVar(self.frame, '10')
        self.end_hour = Spinbox(self.frame, from_=0, to=23, wrap=True, textvariable=self.end_hourstr, width=2,
                                state="readonly")
        self.end_minstr = StringVar(self.frame, '30')
        self.end_minstr.trace("w", self.trace_var)
        self.end_last_value = ""
        self.end_min = Spinbox(self.frame, from_=0, to=59, wrap=True, textvariable=self.end_minstr, width=2,
                               state="readonly")
        self.end_hour.pack(side=LEFT)
        self.end_min.pack(side=LEFT)

        def time_date_str(hour, minute):
            min_str = lambda min: "0" + min if int(min) < 10 else min
            minute = min_str(minute)
            return self.calendar.get_date() + f"/{hour}" + f"/{minute}"

        def run():
            eventscheduler.run_popup(
                time_date_str(
                    self.start_hourstr.get(),
                    self.start_minstr.get()
                )
                ,
                self.entry_event.get(),
                self.entry_descr.get("1.0", "end-1c"),
                self.entry_link.get()
            )
            self.submit_event()

        self.submit_btn = Button(self.frame, text='Submit', command=run)
        self.recur_check = Checkbutton(self.frame, text='Recurring Meeting', command=self.recurring)
        self.recur_check.pack()
        self.submit_btn.pack()

    def trace_var(self, *args):
        if self.start_last_value == "59" and self.start_minstr.get() == "0":
            self.start_hourstr.set(int(self.start_hourstr.get()) + 1 if self.start_hourstr.get() != "23" else 0)
        self.start_last_value = self.start_minstr.get()

    def recurring(self):
        # Make a checkbar with every day of the week
        self.pack()

    def submit_event(self):
        import eventscheduler

        #    if not usersDatabase.check_overlap(self.email, self.give_date(self.calendar.get_date()), time(int(self.start_hourstr.get()), int(self.start_minstr.get())), time(int(self.end_hourstr.get()), int(self.end_minstr.get()))):
        #       pass

        #    print(type(self.start_hourstr.get()))
        #   print(type(self.start_minstr.get()))
        #   print(self.calendar.get_date())

        # exit(-1)
        start_time = self.start_hourstr.get() + ":" + self.start_minstr.get() + ":" + "00"
        end_time = self.end_hourstr.get() + ":" + self.end_minstr.get() + ":" + "00"

        usersDatabase.add_user_info(self.email, self.entry_event.get(), self.entry_link.get(),
                                    self.entry_descr.get('1.0', 'end-1c'),
                                    self.give_date(self.calendar.get_date()), time(int(self.start_hourstr.get()), int(self.start_minstr.get())), time(int(self.end_hourstr.get()), int(self.end_minstr.get())))
        #                          ,time(int(self.start_hourstr.get()), int(self.start_minstr.get())),
        # time(int(self.end_hourstr.get()), int(self.end_minstr.get())))
        # self.display_event()
        self.calendar.destroy()

        self.label_event.destroy()
        self.label_descr.destroy()
        self.label_link.destroy()
        self.entry_event.destroy()
        self.entry_descr.destroy()
        self.entry_link.destroy()
        self.recur_check.destroy()
        self.submit_btn.destroy()
        self.start_hour.destroy()
        self.start_min.destroy()
        self.end_hour.destroy()
        self.end_min.destroy()
        self.start_label.pack_forget()
        self.end_label.pack_forget()
        self.add_button.pack()

    def display_event(self):
        self.r_frame = Frame(self, bg='lightblue').pack(side=RIGHT)
        event = Label(self.r_frame, text='Event: \n' + self.entry_event.get()).pack()
        desc = Label(self.r_frame, text='Description: \n' + self.entry_descr.get('1.0', 'end-1c')).pack()
        link = Label(self.r_frame, text='Link: \n' + self.entry_link.get()).pack()
        times = Label(self.r_frame,
                      text='Start Time: ' + self.start_hourstr.get() + ':' + self.start_minstr.get() + ' End Time: ' + self.end_hourstr.get() + ':' + self.end_minstr.get()).pack()

    def give_time(self, time_str):
        # converts the string to a datetime object

        split_time = time_str.split(":")
        split_time_2 = []
        if (split_time[1][2] == "A"):
            time_str_2 = split_time[1].split("A")[0]
            return time(int(split_time[0]), int(time_str_2))
        else:
            time_str_2 = split_time[1].split("P")[0]
            return time(int(split_time[0]), int(time_str_2))

    def give_date(self, date_str):
        split_date = date_str.split("/")
        return date(int("20" + split_date[2]), int(split_date[0]), int(split_date[1]))


def check_password(password):
    regex = '\d.*?[A-Z].*?[a-z]'
    if not re.search(regex, password) and len(password) < 7:
        print('Password must include an uppercase and lowercase letter, a number and be longer than 7 characters')
        return False
    else:
        return True


def check_confirm_pass(pass_confirm, password):
    if password != pass_confirm:
        print('Passwords and confirm password do not match')
        return False
    else:
        return True


def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        print('Please enter a valid email address')
        return False
    else:
        return True


def check_login(email, password):
    # checks if the email and corresponding password are present in the database
    if loginDatabase.checkCredentials(email, password) == True:
        return True
    else:
        return False


loginDatabase.createDatabase('accessapproved', 'one_click_users')

if __name__ == '__main__':
    page_color = '#00c6d4'
    root = Tk()
    root.title('OneClick - Login')
    root.configure(bg='DarkGoldenrod1')
    root.geometry('1000x1000')
    lw = LoginWindow(root)
    root.mainloop()
