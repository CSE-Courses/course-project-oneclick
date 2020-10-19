import loginDatabase
import datetime


def create_user_table(user_email):
    # creates table with email and password as columns

    mysqldb = loginDatabase.connectToDatabase()
    mcursor = mysqldb.cursor()
    statement = "CREATE TABLE IF NOT EXISTS `{}` (event_name VARCHAR(" \
                "255) PRIMARY KEY, zoom_link " \
                "VARCHAR(255), " \
                "description VARCHAR(255), event_date DATE NOT NULL,start_time TIME NOT NULL, end_time TIME NOT " \
                "NULL)".format(user_email)
    print(statement)
    mcursor.execute(statement)
    print("table created")
    mysqldb.close()


def add_user_info(email,event_name,zoom_link,description,event_date,start_time,end_time):
    # event_date is a date object reference
    # start_time and end_time are time object references
    # email,event_name,zoom_link and description are strings
    create_user_table(email)
    statement = "INSERT INTO `{}` (event_name,zoom_link,description,event_date,start_time,end_time) VALUES(%s,%s,%s,%s,%s,%s)".format(email)
    print(statement)
    mysqldb = loginDatabase.connectToDatabase()
    print("connection done")
    mcursor = mysqldb.cursor()
    print("cursor obtained")
    mcursor.execute(statement,(event_name,zoom_link,description,event_date.strftime("%Y-%m-%d"),start_time.strftime("%H:%M:%S"),end_time.strftime("%H:%M:%S")))
    print("execute done!")
    mysqldb.commit()
    print("user info added")
    mysqldb.close()
# create_user_table("mhertz@buffalo.edu")
# add_user_info("mhertz@buffalo.edu","Garbage Collection","http://java.ociweb.com/mark/other-presentations/JavaGC.pdf","Let's destroy objects with no references pointing to them",datetime.date(2021,11,12),datetime.time(3,30,00),datetime.time(4,55,00))

