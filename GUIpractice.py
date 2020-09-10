import tkinter as tk

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
colors = ["firebrick", "darkorange", "yellow", "springgreen", "royalblue", "indigo", "violet"]

window = tk.Tk()

for x in range(7):
    frame = tk.Frame(master=window, width=100, height=300, bg=colors[x])
    frame.pack(fill=tk.Y, side=tk.LEFT, expand=True)
    label = tk.Label(master=frame, text=days[x], bg="black", fg="white")
    label.place(x=50, y=20, anchor="center")


window.mainloop()
