import mysql.connector


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
    str = "CREATE DATABASE " + nameStr
    mycursor.execute(str)
    print("Database successfully created")

def connectToDatabase():
    # establishes a connection to MySQL database
    mydb = mysql.connector.connect (
        host="localhost",
        user="root",
        password="database123",
        database="oneclickusers"
    )
    return mydb


def addUser(email, password):
    #adds a new user to the database

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
    val = (email, password)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "Record Inserted")

def removeUser(email):

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    emailStr = str(email)
    string = "DELETE FROM users WHERE email = '" + emailStr + "'"
    mycursor.execute(string)
    mydb.commit()
    print(mycursor.rowcount, "User(s) successfully deleted")

def checkDuplicate(email):
    #check to see if this email is already in the database
    # returns 'True' if there is a duplicate

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT email FROM users")

    myresult = mycursor.fetchall()

    for x in myresult:
        y = x[0]            # get first element in table row
        if y == email:
            print("Email address already exists!")
            return True

    return False


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
