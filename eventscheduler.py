import time
import datetime
import threading
import os
import gui_popup 





#inDate = "18/10/2020" 
#inTime = "22/28" 
#DATE str DAY/MONTH/YEAR
#TIME str MILITARY H/M
def run_popup(inDate,inTime,title,desc,link,zoom_position):
    finalDate = inDate + "/" + inTime
    timestamp = time.mktime(datetime.datetime.strptime(finalDate, "%d/%m/%Y/%H/%M").timetuple())
    difference = int(timestamp - time.time())
    def timer():
        zoom_command=gui_popup.zoom_call_command(link,zoom_position)
        gui_popup.event_pop_up(title,desc,zoom_command)    

    print(timestamp - time.time())
    my_timer = threading.Timer(difference, timer)
    my_timer.start()
    print("Waiting...")
