import mysql.connector
from database import usersDatabase


def createDatabase(password, name):
    # creates a localhost database named, "oneclickusers"
    # enter password created when configuring MySQL on computer
    # only needs to be created once
    passwordStr = str(password)
    nameStr = str(name)

    mydb = mysql.connector.connect (
        host="localhost",
        user="root",
        password=passwordStr
    )
    mycursor = mydb.cursor()
    query = "CREATE DATABASE " + nameStr
    mycursor.execute(query)
    print("Database successfully created")

def connectToDatabase():
    # establishes a connection to MySQL database
    mydb = mysql.connector.connect (
        host="localhost",
        user="root",
        password="accessapproved",
        database="one_click_users"
    )
    return mydb

def create_users_table():
    # creates table with email and password as columns
    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS users (email VARCHAR(255), password VARCHAR(20))")
    print("table created")
    mydb.close()


def user_exists(email):

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    sql = "SELECT * from users"
    mycursor.execute(sql)

    rows = mycursor.fetchall()

    for row in rows:
        if row[0] == email:
            return True
        else:
            continue
    return False


def addUser(email, password):
    #adds a new user to the database

    if user_exists(email):
        return
    else:

        mydb = connectToDatabase()
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
        val = (email, password)
        mycursor.execute(sql, val)

        mydb.commit()
        mydb.close()
        print(mycursor.rowcount, "Record Inserted")
        usersDatabase.create_user_table(email)


def removeUser(email):

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    emailStr = str(email)
    string = "DELETE FROM users WHERE email = '" + emailStr + "'"
    mycursor.execute(string)
    mydb.commit()
    mydb.close()
    usersDatabase.drop_user_table(email)
    print(mycursor.rowcount, "User(s) successfully deleted")

def checkCredentials(email,password):
    #check to see if this email is already in the database
    # returns 'True' if there is a duplicate

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")

    myresult = mycursor.fetchall()

    for x in myresult:
        y = x[0]            # get first element in table row
        if y == email:
            print("Correct email!")
            if x[1] == password:
                print("correct password")
                mydb.close()
                return True
            else:
                print(x[1] + ", " + password)
                mydb.close()
                return False
    print("email not found")
    mydb.close()
    return False

'''def checkPassword(password):
    # checks to see if the password entered matches
    # the corresponding email in the database

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT password FROM user")

    myresult = mycursor.fetchall()

    for x in myresult:
        y = x[0]  # get the second element in the table row (which is the password)
        print(x)
        if y == password:
            print("correct password")
            mydb.close()
            return True
        mydb.close()
        return False '''



#def login(email, password):
    # checks if the email, password pair is valid in the database
    # returns True if it is a valid user



def printUsers():
    # prints all users stored in the database

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT email FROM users")

    myresult = mycursor.fetchall()

    for x in myresult:
        y = x[0]
        print(y)



def check_tables():

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    print(mycursor.execute("SHOW TABLES"))



removeUser("einsteine@gmail.com")

