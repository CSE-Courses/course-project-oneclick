import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(host='localhost', user='root',
                              passwd='accessapproved')  # establishes connection with mysql db
cursor = cnx.cursor()  # cursor is used as an object to connect with the data base to execute queries

class Initialize:


    def create_schema(self,my_cursor): # not sure if this is required as of now

        try:
            my_cursor.execute('CREATE DATABASE one_click')
            return True
        except mysql.connector.Error as err:
             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Incorrect username or password')
             elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('database does not exist?')
             else:
                print('unknown error -- returning')
                return False
        return False

    def create_tables(self):
        return False

init = Initialize()
init.create_schema(cursor)



