from tkinter import *
from tkinter import ttk
import re
from tkcalendar import Calendar
from database import loginDatabase
from database import usersDatabase
import datetime
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
        self.img = Label(self.master, image=render, bg='DarkGoldenrod1')
        self.img.image = render
        self.img.place(x=410, y=50)
        self.label_email = Label(self, text='Email', bg=page_color, font='ComicSansMS 25 bold')
        self.label_password = Label(self, text='Password', bg=page_color, font='ComicSansMS 25 bold')
        self.label_create_acct = Label(self, text='Create Account', fg='blue', font='ComicSansMS', cursor='hand2',
                                       bg=page_color)
        self.label_create_acct.bind('<Button-1>', lambda e: self.create_clicked())
        self.label_delete_acct = Label(self, text='Delete Account', fg='blue', font='ComicSansMS', cursor='hand2',
                                       bg=page_color)
        self.label_delete_acct.bind('<Button-1>', lambda e: self.delete_clicked())

        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show='*')

        self.label_email.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.login_button = Button(self, text='Login', font='ComicSansMS 15 bold', fg='lime green',
                                   command=self.login_clicked)
        self.login_button.grid(columnspan=4)
        self.label_create_acct.grid(columnspan=4)
        self.label_delete_acct.grid(columnspan=4)
        self.error_text = StringVar()
        self.error_text.set("")
        self.error_label = Label(self.master, textvariable=self.error_text, bg=page_color, font='veranda 15 bold')
        self.error_label.place(x=390, y=500)
        loginDatabase.create_users_table()

        #self.pack()
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
            self.master.configure(bg='midnight blue')
            app = MainWindow(self.master, email)
        else:
            self.error_label.configure(bg='red')
            self.error_text.set("Incorrect Email or Password")

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

    def delete_clicked(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        self.master.destroy()
        self.master = Tk()
        self.master.title('Delete Account')
        self.master.geometry('1000x1000')
        page_color = '#00c6d4'
        self.master.configure(bg='DarkGoldenrod1')
        app = DeleteAccount(self.master)


class DeleteAccount(Frame):
    def __init__(self, master):
        super().__init__(master)
        page_color = 'DarkGoldenrod1'
        load = Image.open("logo.png")
        zoom = 0.5
        pixels_x, pixels_y = tuple([int(zoom * x) for x in load.size])

        render = ImageTk.PhotoImage(load.resize((pixels_x, pixels_y)))
        self.main_frame = Frame(self.master, width=240, height=720, bg='DarkGoldenrod1')
        self.img = Label(self.master, image=render)
        self.img.image = render
        self.img.place(x=430, y=50)
        self.main_frame.pack()
        Frame.configure(self, bg=page_color)
        self.label_email = Label(self.master, text='Email', bg=page_color, font='ComicSansMS 25 bold')
        self.label_password = Label(self.master, text='Password', bg=page_color, font='ComicSansMS 25 bold')
        self.label_pass_confirm = Label(self.master, text='Confirm Password', bg=page_color, font='ComicSansMS 25 bold')

        self.entry_email = Entry(self.master)
        self.entry_password = Entry(self.master, show='*')
        self.entry_pass_confirm = Entry(self.master, show='*')
        self.label_email.place(x=360, y=320)
        self.label_password.place(x=360, y=360)
        self.label_pass_confirm.place(x=360, y=400)

        self.entry_email.place(x=435, y=330)
        self.entry_password.place(x=480, y=370)
        self.entry_pass_confirm.place(x=580, y=410)

        self.create_button = Button(self.master, text='Delete Account', bg=page_color, fg='brown', font='ComicSansMS',
                                    command=self.delete_account)
        self.cancel_button = Button(self.master, text='Cancel', bg=page_color, fg='brown', font='ComicSansMS',
                                    command=self.delete_cancel)
        self.cancel_button.place(x=400, y=460)
        # self.create_button.grid(columnspan=2)
        self.create_button.place(x=500, y=460)
        self.pack()
        self.error_text = StringVar()
        self.error_text.set("")
        self.error_label = Label(self.master, textvariable=self.error_text, bg=page_color, font='veranda 15 bold')
        self.error_label.place(x=400, y=500)
        # self.place(x=330, y=330)

    def delete_account(self):

        email = self.entry_email.get()
        password = self.entry_password.get()
        confirm_pass = self.entry_pass_confirm.get()
        if(not(password == confirm_pass)):
            self.error_label.configure(bg='red')
            self.error_text.set("Confirm Password does not match Password")
            return
        if (check_login(email, password)):
            usersDatabase.delete_user_account(email)
            self.master.destroy()
            self.master = Tk()
            self.master.title('Hope to see you back again soon!')
            self.master.geometry('1000x1000')
            self.master.configure(bg='DarkGoldenrod1')
            app = LoginWindow(self.master)

        else:
            self.error_label.configure(bg='red')
            self.error_text.set("Incorrect Email or Password")

    def delete_cancel(self):
        self.master.destroy()
        self.master = Tk()
        self.master.title('Welcome to the OneClick Community!')
        self.master.geometry('1000x1000')
        self.master.configure(bg='DarkGoldenrod1')
        app = LoginWindow(self.master)


class CreateAccount(Frame):
    def __init__(self, master):
        super().__init__(master)

        # page_color = '#00c6d4'
        page_color = 'DarkGoldenrod1'
        load = Image.open("logo.png")
        zoom = 0.5
        pixels_x, pixels_y = tuple([int(zoom * x) for x in load.size])

        render = ImageTk.PhotoImage(load.resize((pixels_x, pixels_y)))
        self.main_frame = Frame(self.master, width=240, height=720, bg='DarkGoldenrod1')
        self.img = Label(self.master, image=render)
        self.img.image = render
        self.img.place(x=430, y=50)
        self.main_frame.pack()
        Frame.configure(self, bg=page_color)
        self.label_email = Label(self.master, text='Email', bg=page_color, font='ComicSansMS 25 bold')
        self.label_password = Label(self.master, text='Password', bg=page_color, font='ComicSansMS 25 bold')
        self.label_pass_confirm = Label(self.master, text='Confirm Password', bg=page_color, font='ComicSansMS 25 bold')

        self.entry_email = Entry(self.master)
        self.entry_password = Entry(self.master, show='*')
        self.entry_pass_confirm = Entry(self.master, show='*')

        # self.label_email.grid(row=0, sticky=E)
        # self.label_password.grid(row=1, sticky=E)
        # self.label_pass_confirm.grid(row=2, sticky=E)
        # self.entry_email.grid(row=0, column=1)
        # self.entry_password.grid(row=1, column=1)
        # self.entry_pass_confirm.grid(row=2, column=1)
        self.label_email.place(x=360, y=320)
        self.label_password.place(x=360, y=360)
        self.label_pass_confirm.place(x=360, y=400)

        self.entry_email.place(x=435, y=330)
        self.entry_password.place(x=480, y=370)
        self.entry_pass_confirm.place(x=580, y=410)

        self.create_button = Button(self.master, text='Create Account', bg=page_color, fg='brown', font='ComicSansMS',
                                    command=self.create_account)
        self.cancel_button = Button(self.master, text='Cancel', bg=page_color, fg='brown', font='ComicSansMS',
                                    command=self.create_cancel)
        self.cancel_button.place(x=400, y=460)
        # self.create_button.grid(columnspan=2)
        self.create_button.place(x=500, y=460)
        self.pack()
        # self.place(x=330, y=330)

    def create_cancel(self):
        self.master.destroy()
        self.master = Tk()
        self.master.title('Welcome to the OneClick Community!')
        self.master.geometry('1000x1000')
        self.master.configure(bg='DarkGoldenrod1')
        app = LoginWindow(self.master)

    def create_account(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        pass_confirm = self.entry_pass_confirm.get()
        if check_email(email) and check_password(password) and check_confirm_pass(pass_confirm, password):
            # Confirm account has been created in database
            loginDatabase.addUser(email, password)
            self.create_cancel()
        else:
            self.entry_email.delete(0, 'end')
            self.entry_password.delete(0, 'end')
            self.entry_pass_confirm.delete(0, 'end')


class UpdateWindow(Frame):
    def __init__(self, master, email, event_name, tup, chosen):
        super().__init__(master)
        print(threading.current_thread().name)
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
        return datetime.date(int("20" + split_date[2]), int(split_date[0]), int(split_date[1]))

    def give_time(self, time_str):
        split_time = time_str.split(':')
        hour = int(split_time[0])
        min = int(split_time[1])
        return time(hour, min)

    def submit_clicked(self):
        new_info = self.info_entry.get()
        # print('email:' + self.email + ', event_name:' + self.event_name + ', new_info:' + new_info + ', chosen:' + self.chosen)
        if self.chosen == 'Event Name':
            new_chosen = 'event_name'
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[0], new_info)
        elif self.chosen == 'Description':
            usersDatabase.update_user_string(self.email, self.event_name, self.chosen, self.tup[1], new_info)
        elif self.chosen == 'Zoom Link':
            new_chosen = 'zoom_link'
            print('zoom link chosen now executing statement')
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[2], new_info)
        elif self.chosen == 'Date':
            new_date = self.give_date(new_info).strftime("%Y-%m-%d")
            print('here')
            new_chosen = 'event_date'
            # print('new date:' + new_date)
            # print('old date:' + self.tup[3].strftime("%m %d %Y"))
            # print(self.email + ', ' + self.event_name + ', ' + new_chosen)
            usersDatabase.update_user_string(self.email, self.event_name, new_chosen, self.tup[3], new_date)
        elif self.chosen == 'Start Time':
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
        self.img = Label(self.master, image=render, bg='midnight blue')
        self.img.image = render
        self.img.place(x=300, y=40)

        self.frame = Frame(master, width=240, height=720, bg='DarkGoldenrod1')
        self.frame.pack(side=LEFT, fill=BOTH)
        self.add_button = Button(self.frame, text='Make Appointment', font='verdana 16 bold', fg='midnight blue',
                                 command=self.create_event)
        self.event_frame = Frame(master, width=240, height=720, bg='DarkGoldenrod1')
        self.event_frame.pack(side=RIGHT, fill=BOTH)
        self.event_canvas = Canvas(self.event_frame, bg='DarkGoldenrod1')
        self.event_canvas.pack(side=LEFT, fill=BOTH)
        self.scroll = Scrollbar(self.event_frame, bg='DarkGoldenrod1', orient=VERTICAL,
                                    command=self.event_canvas.yview)
        self.scroll.pack(side=LEFT, fill=Y)
        self.event_canvas.configure(yscrollcommand=self.scroll.set)
        self.event_canvas.bind('<Configure>',
                               lambda e: self.event_canvas.configure(scrollregion=self.event_canvas.bbox("all")))
        self.inner_frame = Frame(self.event_canvas, bg='DarkGoldenrod1')
        self.event_canvas.create_window((0, 0), window=self.inner_frame, anchor="ne")

        self.variable = StringVar(self.event_frame)
        self.my_events_label = Label(self.inner_frame, text="My Events", bg='lightblue', font='verdana 16 bold', padx=1,
                                     pady=1)

        # self.event_one_label = Label(self.event_frame, text="Event One", bg='lightpink', font='bold', padx=20, pady=20)

        def dynamic_delete(event_name):
            usersDatabase.delete_user_event(self.email, event_name)
            self.master.destroy()
            self.master = Tk()
            self.master.title('OneClick')
            self.master.geometry('1280x720')
            self.master.configure(bg='midnight blue')
            app = MainWindow(self.master, email)

        def up_event_clicked(event_name, tup):

            chosen = self.option()
            # self.master.destroy()
            self.new_root = Tk()
            title = 'Enter new ' + chosen
            if chosen == 'Date':
                title = 'Enter new date in mm/dd/yy format'
            if chosen == 'Start Time':
                title = 'Enter new start time in hh:mm format'
            if chosen == 'End Time':
                title = 'Enter new end time in hh:mm format'
            self.new_root.title(title)
            self.new_root.geometry('500x500')
            self.new_root.configure(bg='DarkGoldenrod1')
            UpdateWindow(self.new_root, email, event_name, tup, chosen)

        def refresh():
            event_dict = usersDatabase.get_user_events(self.email)
            #   for widget in self.event_frame.winfo_children():
            #      widget.destroy()
            self.my_events_label.pack()
            # self.event_one_label.pack()

            for key in event_dict:
                tup = event_dict[key]
                size = len(tup)
                dat = tup[2].strftime('%m %d %Y')
                str_date = dat.split(' ')
                new_date = str_date[0] + '/' + str_date[1] + '/' + str_date[2]
                info = key + '\n' + 'Description:' + tup[1] + '\n' + 'Zoom Link:' + tup[
                    0] + '\n' + 'Date:' + new_date + '\n' + 'Start Time:' + str(tup[3]) + '\n' + 'End Time:' + str(
                    tup[4])
                self.pass_tuple = (key, tup[1], tup[0], tup[2], tup[3], tup[4])
                option_list = ['Event Name', 'Zoom Link', 'Description', 'Date', 'Start Time', 'End Time']
                # self.variable = StringVar(self.event_frame)
                print(type(tup[3]))
                print(str(tup[3]))

                def is_completed():
                    stime_str = str(tup[3]).split(':')
                    etime_str = str(tup[4]).split(':')
                    now_str = datetime.datetime.now().strftime('%H %M').split(' ')
                    d = datetime.date.today()
                    today_str_date = d.strftime('%m %d %Y').split(' ')

                    print(str_date[2] + ', ' + today_str_date[2])

                    if ((int(str_date[1]) == int(today_str_date[1])) and (
                            int(str_date[2]) == int(today_str_date[2])) and (
                            int(str_date[0]) == int(today_str_date[0]))):
                        if (int(etime_str[0]) < int(now_str[0])):
                            return 'brown'
                        if ((int(etime_str[1]) < int(now_str[1]) and (int(etime_str[0]) == int(now_str[0])))):
                            return 'brown'
                        if (int(stime_str[0]) < int(now_str[0])):
                            print('yes4')
                            return 'green'
                        elif ((int(stime_str[1]) <= int(now_str[1])) and (int(stime_str[0]) == int(now_str[0]))):
                            print(stime_str[1] + ', ' + now_str[1])
                            print('yes5')
                            return 'green'
                        else:
                            return 'red'

                    elif (int(str_date[2]) < int(today_str_date[2])):
                        return 'brown'
                    elif ((int(str_date[2]) == int(today_str_date[2])) and (int(str_date[0]) < int(today_str_date[0]))):
                        return 'brown'
                    elif ((int(str_date[2]) == int(today_str_date[2])) and (
                            int(str_date[0]) == int(today_str_date[0])) and (
                                  int(str_date[1]) < int(today_str_date[1]))):
                        return 'brown'

                    else:
                        if (int(str_date[2]) > int(today_str_date[2])):
                            return 'red'
                        if (int(str_date[2]) < int(today_str_date[2])):
                            print('yes1')
                            return 'green'
                        elif ((int(str_date[0]) < int(today_str_date[0])) and (
                                int(str_date[2]) == int(today_str_date[2]))):
                            print('yes2')
                            return 'green'
                        elif ((int(str_date[1]) < int(today_str_date[1])) and (
                                int(str_date[2]) == int(today_str_date[2])) and (
                                      int(str_date[0]) == int(today_str_date[0]))):
                            print('yes3')
                            return 'green'
                        else:
                            return 'red'

                self.event = Label(self.inner_frame, text=info, bg='lightpink', font='bold', padx=15, pady=20)

                if (is_completed() == 'green'):
                    self.event = Label(self.inner_frame, text=info, bg='green3', font='verdana 12', padx=15, pady=20)
                elif (is_completed() == 'brown'):
                    self.event = Label(self.inner_frame, text=info, bg='light pink', font='verdana 12', padx=15,
                                       pady=20)
                else:
                    self.event = Label(self.inner_frame, text=info, bg='MediumOrchid1', font='verdana 12', padx=15,
                                       pady=20)

                self.event.pack()
                self.variable.set(option_list[0])
                self.variable.trace("w", self.option)
                self.update_options = OptionMenu(self.inner_frame, self.variable, *option_list)
                self.update_options.pack()
                self.update_button = Button(self.inner_frame, text='Update', font='veranda 14 bold', fg='midnight blue',
                                            command=lambda i=key: up_event_clicked(i, self.pass_tuple))
                self.update_button.pack()
                self.del_button = Button(self.inner_frame, text='Delete', font='veranda 14 bold', fg='midnight blue',
                                         command=lambda i=key: dynamic_delete(i))
                self.del_button.pack()

        ref_func = refresh()

        self.logout_button = Button(self.frame, text='Logout', font='verdana 16 bold', fg='midnight blue',
                                    command=self.logout)
        self.add_button.pack()
        self.logout_button.pack()

    def option(self, *args):
        return self.variable.get()

    def logout(self):
        self.master.destroy()
        new_root = Tk()
        new_root.title('OneClick - Login')
        new_root.configure(bg='DarkGoldenrod1')
        new_root.geometry('1000x1000')
        lw = LoginWindow(new_root)
        new_root.mainloop()

    def create_event(self):

        # TODO: use grid and create spacing between widgets in self.frame, also place submit button in the bottom-middle

        self.logout_button.destroy()
        self.new_logout_button = Button(self.frame, text='Logout', font='verdana 14 bold', fg='midnight blue',
                                        command=self.logout)
        self.add_button.pack_forget()
        self.calendar = Calendar(self.frame, font='Arial 14', bg='midnight blue', fg='midnight blue', cursor='dotbox',
                                 selectmode='day',
                                 showothermonthdays=False, showweeknumbers=False, firstweekday='sunday')
        self.label_event = Label(self.frame, text='Event Name', font='veranda 14 bold', bg='DarkGoldenrod1',
                                 fg='midnight blue')
        self.label_descr = Label(self.frame, text='Description', font='veranda 14 bold', bg='DarkGoldenrod1',
                                 fg='midnight blue')
        self.label_command = Label(self.frame, text='Application Selection', font='veranda 14 bold',
                                   bg='DarkGoldenrod1', fg='midnight blue')
        self.label_link = Label(self.frame, text='Zoom Link', font='veranda 14 bold', bg='DarkGoldenrod1',
                                fg='midnight blue')

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

        self.start_label = Label(self.frame, text='Start Time: ', bg='DarkGoldenrod1', font='veranda 14 bold',
                                 fg='midnight blue')
        self.start_label.place(x=20, y=450)
        self.start_hourstr = StringVar(self.frame, '10')
        self.start_hour = Spinbox(self.frame, font='veranda 14 bold', fg='midnight blue', from_=0, to=23, wrap=True,
                                  textvariable=self.start_hourstr, width=2,
                                  state="readonly")
        self.start_minstr = StringVar(self.frame, '30')
        self.start_minstr.trace("w", self.trace_var)
        self.start_last_value = ""
        self.start_min = Spinbox(self.frame, font='veranda 14 bold', fg='midnight blue', from_=0, to=59, wrap=True,
                                 textvariable=self.start_minstr, width=2,
                                 state="readonly")
        self.start_hour.place(x=133, y=450)
        self.start_min.place(x=173, y=450)

        self.end_label = Label(self.frame, text='End Time: ', bg='DarkGoldenrod1', font='veranda 14 bold',
                               fg='midnight blue')
        self.end_label.place(x=220, y=450)
        self.end_hourstr = StringVar(self.frame, '10')
        self.end_hour = Spinbox(self.frame, font='veranda 14 bold', fg='midnight blue', from_=0, to=23, wrap=True,
                                textvariable=self.end_hourstr, width=2,
                                state="readonly")
        self.end_minstr = StringVar(self.frame, '30')
        self.end_minstr.trace("w", self.trace_var)
        self.end_last_value = ""
        self.end_min = Spinbox(self.frame, font='veranda 14 bold', fg='midnight blue', from_=0, to=59, wrap=True,
                               textvariable=self.end_minstr, width=2,
                               state="readonly")
        self.end_hour.place(x=326, y=450)
        self.end_min.place(x=366, y=450)

        def time_date_str(hour, minute):
            min_str = lambda min: "0" + min if int(min) < 10 else min
            minute = min_str(minute)
            return self.calendar.get_date() + f"/{hour}" + f"/{minute}"

        def check_conflict():
            event_dict = usersDatabase.get_user_events(self.email)
            #   for widget in self.event_frame.winfo_children():
            #      widget.destroy()
            self.my_events_label.pack()
            # self.event_one_label.pack()

            for key in event_dict:
                tup = event_dict[key]
                size = len(tup)
                dat = tup[2].strftime('%m %d %Y')
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                print(type(tup[2]))
                print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                if(tup[2] == self.give_date(self.calendar.get_date())):
                    st_time = time(int(self.start_hourstr.get()), int(self.start_minstr.get()))
                    end_time = time(int(self.end_hourstr.get()), int(self.end_minstr.get()))
                    est_time = (datetime.datetime.min + tup[3]).time()
                    eend_time = (datetime.datetime.min + tup[4]).time()
                    print(est_time)
                    print(st_time)
                    print(end_time)
                    if((st_time >= est_time) and (st_time <= eend_time)):
                        return str(key)
                    elif((end_time>=est_time) and (eend_time <= end_time)):
                        return str(key)
                    elif((st_time >= est_time) and (eend_time >= est_time) and (eend_time <= end_time)):
                        return str(key)
                    elif((st_time <= est_time) and (est_time <= end_time)):
                        return str(key)
                    

            return None


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
            ret_val = check_conflict()
            if(not(ret_val == None)):
                print('Yes there is a conflict -- returning now!')
                self.error_text.set('Unable to create event, conflict with:{}'.format(ret_val))
                self.error_label.configure(bg='red')
                return
            else:
                self.submit_event()

        self.submit_btn = Button(self.frame, text='Submit', font='veranda 14 bold', fg='midnight blue', command=run)
        self.error_text = StringVar()
        self.error_text.set("")
        self.error_label = Label(self.master, textvariable=self.error_text, bg='DarkGoldenrod1', font='veranda 15 bold')
        self.submit_btn.place(x=230, y=490)
        self.new_logout_button.place(x=0, y=0)
        self.error_label.place(x=80, y=530)

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
                                    self.give_date(self.calendar.get_date()),
                                    time(int(self.start_hourstr.get()), int(self.start_minstr.get())),
                                    time(int(self.end_hourstr.get()), int(self.end_minstr.get())))
        self.master.destroy()
        self.master = Tk()
        self.master.title('OneClick')
        self.master.geometry('1280x720')
        self.master.configure(bg='midnight blue')
        app = MainWindow(self.master, self.email)

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
        return datetime.date(int("20" + split_date[2]), int(split_date[0]), int(split_date[1]))


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
