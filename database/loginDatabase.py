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

def create_table():
    # creates table with email and password as columns
    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE users (email VARCHAR(255), password VARCHAR(20),event_name VARCHAR(255),zoom_link "
                     "VARCHAR(255),description VARCHAR(255),event_date DATE NOT NULL, start_time TIME NOT NULL, "
                     "end_time TIME NOT NULL)")
    print("table created")
    mydb.close()


def addUser(email, password):
    #adds a new user to the database

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    sql = "INSERT INTO user (email, password) VALUES (%s, %s)"
    val = (email, password)
    mycursor.execute(sql, val)

    mydb.commit()
    mydb.close()
    print(mycursor.rowcount, "Record Inserted")

def removeUser(email):

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    emailStr = str(email)
    string = "DELETE FROM users WHERE email = '" + emailStr + "'"
    mycursor.execute(string)
    mydb.commit()
    mydb.close()
    print(mycursor.rowcount, "User(s) successfully deleted")

def checkCredentials(email,password):
    #check to see if this email is already in the database
    # returns 'True' if there is a duplicate

    mydb = connectToDatabase()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user")

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
                print("incorrect password")
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



