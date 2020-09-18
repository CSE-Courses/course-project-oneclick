from tkinter import *
import re

class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
    
        self.label_username = Label(self, text='Username')
        self.label_password = Label(self, text='Password')
        self.label_create_acct = Label(self, text='Create Account', fg='blue', cursor='hand2')
        self.label_create_acct.bind('<Button-1>', lambda e: self.create_clicked())
    
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show='*')
        
        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
    
        self.login_button = Button(self, text='Login', command=self.login_clicked)
        self.login_button.grid(columnspan=2)
        self.label_create_acct.grid(columnspan=2)
        
        self.pack()
    
    def login_clicked(self):
        # Check database for username and password and allow/disallow access
        username = self.entry_username.get()
        password = self.entry_password.get()
        check_password(password)
        print(username)
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
        self.label_username = Label(self, text='Username')
        self.label_password = Label(self, text='Password')
        self.label_pass_confirm = Label(self, text='Confirm Password')
        
        self.entry_email = Entry(self)
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show='*')
        self.entry_pass_confirm = Entry(self, show='*')
        
        self.label_email.grid(row=0, sticky=E)
        self.label_username.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)
        self.label_pass_confirm.grid(row=3, sticky=E)
        self.entry_email.grid(row=0, column=1)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)
        self.entry_pass_confirm.grid(row=3, column=1)
        
        self.create_button = Button(self, text='Create Account', command=self.create_account)
        self.create_button.grid(column=1)
        
        self.pack()
        
    def create_account(self):
        email = self.entry_email.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        pass_confirm = self.entry_pass_confirm.get()
        
        check_email(email)
        if password != pass_confirm: print('Password and confirm password do not match')
        return

def check_password(password):
    regex = '\d.*?[A-Z].*?[a-z]'
    if not re.search(regex, password) and len(password) < 7:
        print('Password must include an uppercase and lowercase letter, a number and be longer than 7 characters')
    
def check_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email): print('Please enter a valid email address')

if __name__ == '__main__':       
    root = Tk()
    root.title('OneClick - Login')
    root.geometry('300x100')
    lw = LoginWindow(root)
    root.mainloop()
