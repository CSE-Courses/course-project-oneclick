import time
import datetime
import threading
import os
import gui_popup 




#inDate = "18/10/2020" 
#inTime = "22/28" 
#DATE str DAY/MONTH/YEAR
#TIME str MILITARY H/M

def change_time(time_str,time,func):
    (month,day,year,hour,minute) = time_str.split('/')
    def len_month(month,year):
        return str([None,31,
            29 if year %4 ==0 else 28,
            31,30,31,30,31,31,30,31,30,31 ][month] )
    if int(minute) < 5:
        if hour == '00':
            if day == '1':
                if month == '1':
                    return  "12" + '/' + len_month(int(month),int(year)) + '/' + str(int(year)-1) + '/' + "23" + '/' + str(func(60+int(minute),time)) 
                else:                 
                    return  str(int(month)-1) + '/' + len_month(int(month),int(year)) + '/' + year + '/' + "23" + '/' + str(func(60+int(minute),time ) )
            else: 
                return  month + '/' + day + '/' + year + '/' + "23" + '/' + str( func( 60+int(minute),time ) ) 
        else:   
            return  month + '/' + day + '/' + year + '/' + str(int(hour)-1) + '/' + str( func(60+int(minute),time))
    else:
        return month + '/' + day + '/' + year + '/' + hour + '/' + str(func(int(minute),time))
 
#def create_notification(event_name,time_before,time_of_event):     
#    finalDate = change_time(time_of_event,time_before,lambda a,b:a-b)
#    timestamp = time.mktime(datetime.datetime.strptime(finalDate, "%m/%d/%y/%H/%M").timetuple())
#    difference = int(timestamp - time.time())
#    def timer():
#        gui_popup.notification_start(event_name,time_before)         
#
#    my_timer = threading.Timer(difference, timer) 
#    my_timer.start()
#    print("Waiting notify...")
def run_popup(finalDate,title,desc,link):
    #create_notification(title,5,finalDate)
    timestamp = time.mktime(datetime.datetime.strptime(finalDate, "%m/%d/%y/%H/%M").timetuple())
    difference = int(timestamp - time.time())
    print(finalDate,datetime.datetime.now().strftime("%m/%d/%y/%H/%M"))
    print(timestamp,time.time())
    print(difference)
    def timer():
        zoom_command=gui_popup.zoom_call_command(link)
        gui_popup.event_pop_up(title,desc,zoom_command)    

    my_timer = threading.Timer(difference, timer)
    my_timer.start()
    print("Waiting...")
