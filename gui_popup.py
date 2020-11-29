import tkinter as tk
from tkinter import CENTER
from tkinter import ttk
from datetime import datetime
import time
import eventscheduler
import os
#import gi
#gi.require_version('Notify', '0.7')
#from gi.repository import Notify
TITLE_FONT= ("Verdana", 20)
BODY_FONT = ("Verdana", 12)
import webbrowser
def run_on_click(popup,command):
    popup.destroy()
    command()

def zoom_call_command(link):
    return lambda : webbrowser.open(link)

run = True
def toggle_run(popup): 
    popup.destroy()
    global run
    run = False 

def event_pop_up(event_title,desc,command):
    
    if not run:return
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=event_title,anchor=CENTER, font=TITLE_FONT)
    label.pack(side="top", fill="x", pady=10)

    label = ttk.Label(popup, text=desc,anchor=CENTER, font=BODY_FONT)
    label.pack(side="top", fill="x", pady=10)

    B1 = ttk.Button(popup, text="Open", command =lambda : run_on_click(popup,command) )
    
    B2 = ttk.Button(popup, text="Do Not Disturb", command =lambda : toggle_run(popup)  )
    B3=ttk.Button(popup,text="Snooze", command=lambda :snooze(popup,command))
    B1.pack()
    B2.pack()
    B3.pack()
    popup.mainloop()

#returns finalDate for "run_popup" input parameter
def snooze(popup,link):
    #snooze for 1 minute
    snooze_time = 1
    snooze_timestamp = snooze_time * 60
    ts = time.time()
    future_ts = ts + snooze_timestamp
    snooze_date = datetime.fromtimestamp(future_ts).strftime("%m/%d/%y/%H/%M")
    eventscheduler.run_popup(str(snooze_date),"Snooze","Appointment Reminder",link)
    popup.destroy()
    return snooze_date


'''def notification_start(event_name,time_till):
    Notify.init(event_name)
    notification = Notify.Notification(summary=f"{event_name}|in {time_till} minutes")
    notification.show() '''

#notification_start("zoom","5")
