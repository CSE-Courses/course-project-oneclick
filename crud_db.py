import mysql.connector
from mysql.connector import errorcode

class Crud:
    cnx = mysql.connector.connect(host='localhost',user='root',passwd='accessapproved') # establishes connection with mysql db
    cursor = cnx.cursor() # cursor is used as an object to connect with the data base to execute queries

    def create_event(self,event_name,st_time,end_time,date,frequency,decription,zoomlink):
        '''returns true if event was successfully created'''
        return False

    def update_event(self,event_name,st_time,end_time,date,frequency,description,zoomlink):
        '''returns true if event was successfully updated'''
        return True

    def read_days_event(self):
        '''returns a list of tuples, each element of the tuple being an event'''
        return []

    def get_event_info(self,event_name,st_time,end_time,date):
        '''returns a tuple which has event info'''
        return ()

    def del_event(self,event_name,st_time,end_time,date):
        '''returns true if deletion was successful'''
        return False
    cnx.close()