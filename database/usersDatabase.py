import loginDatabase
import mysql.connector
import datetime

def connectToDatabase():
    # establishes a connection to MySQL database
    mydb = mysql.connector.connect (
        host="localhost",
        user="root",
        password="accessapproved",
        database="one_click_users"
    )
    return mydb

def create_user_table(user_email):
    # creates table with email and password as columns

    mysqldb = connectToDatabase()
    mcursor = mysqldb.cursor()
    statement = "CREATE TABLE IF NOT EXISTS `{}` (event_name VARCHAR(" \
                "255) PRIMARY KEY, zoom_link " \
                "VARCHAR(255), " \
                "description VARCHAR(255), event_date DATE NOT NULL,start_time TIME NOT NULL, end_time TIME NOT " \
                "NULL)".format(change_email(user_email))
   # print(statement)
    mcursor.execute(statement)
   # print("table created")
    mysqldb.close()

def change_email(email):

    split_email = email.split("@")
    split_email_again = split_email[1].split(".")
    return split_email[0]+"_"+split_email_again[0]+"_"+split_email_again[1]

def add_user_info(email,event_name,zoom_link,description,event_date,start_time,end_time):
    # event_date is a date object reference
    # start_time and end_time are time object references
    # email,event_name,zoom_link and description are strings
    create_user_table(email)
    statement = "INSERT INTO `{}` (event_name,zoom_link,description,event_date,start_time,end_time) VALUES(%s,%s,%s,%s,%s,%s)".format(change_email(email))
   # print(statement)
    mysqldb = connectToDatabase()
    #print("connection done")
    mcursor = mysqldb.cursor()
    #print("cursor obtained")
    mcursor.execute(statement,(event_name,zoom_link,description,event_date.strftime("%Y-%m-%d"),start_time,end_time))
    #print("execute done!")
    mysqldb.commit()
    #print("user info added")
    mysqldb.close()
# create_user_table("mhertz@buffalo.edu")
# add_user_info("mhertz@buffalo.edu","Garbage Collection","http://java.ociweb.com/mark/other-presentations/JavaGC.pdf","Let's destroy objects with no references pointing to them",datetime.date(2021,11,12),datetime.time(3,30,00),datetime.time(4,55,00))

def change_email(email):

    split_email = email.split("@")
    split_email_again = split_email[1].split(".")
    return split_email[0]+"_"+split_email_again[0]+"_"+split_email_again[1]

def get_user_events(email):

    # takes in user email and returns a dictionary

    new_email = change_email(email)
    mysqldb = connectToDatabase()
    cursor = mysqldb.cursor()
    statement = "SELECT * FROM {}".format(new_email)
    cursor.execute(statement)
    rows = cursor.fetchall()
    ret_dict = {}

    for row in rows:
        ret_dict[row[0]] = row[1:6]
    mysqldb.close()
    return ret_dict

def drop_user_table(email):

    mysql = connectToDatabase()
    cursor = mysql.cursor()
    cursor.execute("DROP TABLE {}".format(change_email(email)))
    mysql.close()


def update_user_event(email,event_name,tuple):
   pass

def delete_user_event(email,event_name):

    try:
        new_email = change_email(email)
        mysqldb = connectToDatabase()
        cursor = mysqldb.cursor()
        statement = "DELETE FROM {} WHERE event_name = '{}'".format(new_email, event_name)
        cursor.execute(statement)
        mysqldb.commit()
        #print(cursor.rowcount(), "record deleted")

    except mysql.connector.Error as error:
        print(error)

    finally:
        cursor.close()
        mysqldb.close()


'''def check_overlap(email,date,start_time,end_time):
    new_email = change_email(email)
    mysqldb = connectToDatabase()
    cursor = mysqldb.cursor()
    statement = "SELECT * FROM {}".format(new_email)
    cursor.execute(statement)
    rows = cursor.fetchall()


    for row in rows:
        print(type(row[3]))
        print(type(row[4]))
        print(type(row[5]))
        print('----------------------')


check_overlap('atri@buffalo.edu', 5, 6, 7)'''




'''dic = get_user_events('jzola@buffalo.edu')
dict(dic)
print(dic)

tup = dic['Comp Sci for Kids']

print(type(tup[2])) '''

#delete_user_event("einsteine98@gmail.com", "random event")


