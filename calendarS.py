import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

#calendar default page 

root = tk.Tk()

def showCalendar():
    def print_sel():
        print(cal.selection_get())

    top = tk.Toplevel(root)

    ttk.Button(top, text="make appointment", command=print_sel).pack()
    cal = Calendar(top,
                   font="Arial 14", cursor="dotbox", selectmode='day', showothermonthdays=False,
                   showweeknumbers=False, firstweekday="sunday")
    cal.pack(fill="both")


ttk.Button(root, text='Calendar', command=showCalendar).pack()

root.mainloop()
