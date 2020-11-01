from tkinter import *
import re
from tkcalendar import Calendar 

class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
    
        self.label_email = Label(self, text='Email')
        self.label_password = Label(self, text='Password')
        self.label_create_acct = Label(self, text='Create Account', fg='blue', cursor='hand2')
        self.label_create_acct.bind('<Button-1>', lambda e: self.create_clicked())
    
        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show='*')
        
        self.label_email.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
    
        self.login_button = Button(self, text='Login', command=self.login_clicked)
        self.login_button.grid(columnspan=2)
        self.label_create_acct.grid(columnspan=2)
        
        self.pack()
    
    def login_clicked(self):
        # Check database for username and password and allow/disallow access
        email = self.entry_email.get()
        password = self.entry_password.get()
        if check_login(email, password):
            self.master.destroy()
            self.master = Tk()
            self.master.title('OneClick')
            self.master.geometry('1280x720')
            app = MainWindow(self.master)
        print(email)
        print(password)
        
    def create_clicked(self):
        self.master.destroy()
        self.master = Tk()
        self.master.title('Create Account')
        self.master.geometry('300x150')
        app = CreateAccount(self.master)
   
class CreateAccount(Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label_email = Label(self, text='Email')
        self.label_password = Label(self, text='Password')
        self.label_pass_confirm = Label(self, text='Confirm Password')
        
        self.entry_email = Entry(self)
        self.entry_password = Entry(self, show='*')
        self.entry_pass_confirm = Entry(self, show='*')
        
        self.label_email.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.label_pass_confirm.grid(row=2, sticky=E)
        self.entry_email.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.entry_pass_confirm.grid(row=2, column=1)
        
        self.create_button = Button(self, text='Create Account', command=self.create_account)
        self.create_button.grid(columnspan=2)
        
        self.pack()
        
    def create_account(self):
        email = self.entry_email.get()
        password = self.entry_password.get()
        pass_confirm = self.entry_pass_confirm.get()
        if check_email(email) and check_password(password) and check_confirm_pass(pass_confirm, password): 
            # Confirm account has been created in database
            self.master.destroy()
            self.master = Tk()
            self.master.title('Login')
            self.master.geometry('300x100')
            app = LoginWindow(self.master)
        else: 
            self.entry_email.delete(0, 'end')
            self.entry_password.delete(0, 'end')
            self.entry_pass_confirm.delete(0, 'end')
            
class MainWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        
        self.frame = Frame(master, width=240, height=720, bg='red')
        self.frame.pack(side=LEFT, fill=BOTH)
        self.add_button = Button(self.frame, text='Make Appointment', command=self.create_event)
        self.add_button.pack()
        
#    def create_event(self):
#        self.label_event = Label(self, text='Event Name')
#        self.label_descr = Label(self, text='Description')
#        self.label_link = Label(self, text='Zoom Link')
# #       self.label_path = Label(self, test='Zoom path')
#
#        self.entry_event = Entry(self, width=64)
#        self.entry_descr = Entry(self, width=64)
#        self.entry_link = Entry(self, width=64)
# #       self.entry_path = Entry(self, width=64)
#        
#        self.label_event.grid(row=1, sticky=E)
#        self.label_descr.grid(row=2, sticky=E)
#        self.label_link.grid(row=3, sticky=E)
# #       self.label_path.grid(row=6, sticky=E)
#        
#        self.entry_event.grid(row=1, column=1)
#        self.entry_descr.grid(row=2, column=1)
#        self.entry_link.grid(row=3, column=1)
# #       self.entry_path.grid(row=6, column=1)
#        
#        string = ':00'
#        option_list = []
#        var = StringVar(self)
#        option_list.append('12:00AM')
#        var.set(option_list[0])
#        for i in range(1,12):
#            option_list.append(str(i) + string + 'AM')
#        option_list.append('12:00PM')
#        for i in range(1,12):
#            option_list.append(str(i) + string + 'PM')
#        self.label_start = Label(self, text='Start Time').grid(row=4, column=0)
#        self.label_end = Label(self, text='End Time').grid(row=4, column=1)
#        self.start_time = OptionMenu(self, var, *option_list)
#        self.start_time.config(width=10)
#        self.end_time = OptionMenu(self, var, *option_list)
#        self.end_time.config(width=10)
#        self.start_time.grid(row=5, column=0)
#        self.end_time.grid(row=5, column=1)
#         
#        self.submit_btn = Button(self, text='Submit', command = summit )
#        self.recur_check = Checkbutton(self, text='Recurring Meeting', command=self.recurring)
#        self.recur_check.grid(columnspan=2)
#        self.submit_btn.grid(columnspan=2)
#        self.pack()
#        
#        self.frame = Frame(master, width=240, height=720, bg='red')
#        self.frame.pack(side=LEFT, fill=BOTH)
#        self.add_button = Button(self.frame, text='Make Appointment', command=self.create_event)
#        self.add_button.pack()
        
    def create_event(self):
        self.add_button.pack_forget()
        self.calendar = Calendar(self.frame, font='Arial 14', cursor='dotbox', selectmode='day',
                                 showothermonthdays=False, showweeknumbers=False, firstweekday='sunday')
        self.label_event = Label(self.frame, text='Event Name')
        self.label_descr = Label(self.frame, text='Description')
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
        self.start_label.pack(side=LEFT, padx=(20,0))
        self.start_hourstr=StringVar(self.frame,'10')
        self.start_hour = Spinbox(self.frame,from_=0,to=23,wrap=True,textvariable=self.start_hourstr,width=2,state="readonly")
        self.start_minstr=StringVar(self.frame,'30')
        self.start_minstr.trace("w",self.trace_var)
        self.start_last_value = ""
        self.start_min = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self.start_minstr,width=2,state="readonly")
        self.start_hour.pack(side=LEFT)
        self.start_min.pack(side=LEFT, padx = (0,20))
        
        self.end_label = Label(self.frame, text='End Time: ')
        self.end_label.pack(side=LEFT)
        self.end_hourstr=StringVar(self.frame,'10')
        self.end_hour = Spinbox(self.frame,from_=0,to=23,wrap=True,textvariable=self.end_hourstr,width=2,state="readonly")
        self.end_minstr=StringVar(self.frame,'30')
        self.end_minstr.trace("w",self.trace_var)
        self.end_last_value = ""
        self.end_min = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self.end_minstr,width=2,state="readonly")
        self.end_hour.pack(side=LEFT)
        self.end_min.pack(side=LEFT)
        import eventscheduler
        c = lambda: eventscheduler.run_popup(
               eventscheduler.to_time_string(f"{calendar.month}/{calendar.day}/{calendar.year}",hourstr.get()),  
               self.entry_event.get(),
               self.entry_descr.get("1.0","end-1c"),
               self.entry_link.get(),
               "zoom"
               ) 
        def run ():
            c
            self.submit_event()

        self.submit_btn = Button(self.frame, text='Submit', command=run)
        self.recur_check = Checkbutton(self.frame, text='Recurring Meeting', command=self.recurring)
        self.recur_check.pack()
        self.submit_btn.pack()
        
    def trace_var(self,*args):
        if self.start_last_value == "59" and self.start_minstr.get() == "0":
            self.start_hourstr.set(int(self.hourstr.get())+1 if self.start_hourstr.get() !="23" else 0)
        self.start_last_value = self.start_minstr.get()
    
    def recurring(self):
        # Make a checkbar with every day of the week
        self.pack()
        
    def submit_event(self):
        import eventscheduler
        
        self.display_event()
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
        times = Label(self.r_frame, text='Start Time: ' + self.start_hourstr.get() + ':' + self.start_minstr.get() + ' End Time: ' + self.end_hourstr.get() + ':' + self.end_minstr.get()).pack()
        
        
def check_password(password):
    regex = '\d.*?[A-Z].*?[a-z]'
    if not re.search(regex, password) and len(password) < 7:
        print('Password must include an uppercase and lowercase letter, a number and be longer than 7 characters')
        return False
    else: return True
    
def check_confirm_pass(pass_confirm, password):
    if password != pass_confirm:
        print('Passwords and confirm password do not match')
        return False
    else: return True
    
def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email): 
        print('Please enter a valid email address')
        return False
    else: return True
    
def check_login(email, password):

    # checks if the email and corresponding password are present in the database
    #if loginDatabase.checkCredentials(email,password) == True:
        return True
    #else:
    #    return False

if __name__ == '__main__':       
    root = Tk()
    root.title('OneClick - Login')
    root.geometry('300x100')
    lw = LoginWindow(root)
    root.mainloop()
