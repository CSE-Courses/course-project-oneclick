import time
import datetime
import threading
import os

    # The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def timer():
    # Calling the function
    notify(title = 'One Click',
              subtitle = 'event started',
              message  = 'Your event is ready!')
    print("I'm working...")


inDate = input("Enter Event Date (day/month/year): ")
inTime = input("Enter Event Time (hour/minute): ")

finalDate = inDate + "/" + inTime
#finalDate = "13/10/2020/00/43"

timestamp = time.mktime(datetime.datetime.strptime(finalDate, "%d/%m/%Y/%H/%M").timetuple())

difference = int(timestamp - time.time())

my_timer = threading.Timer(difference, timer)
my_timer.start()
print("Waiting...")
