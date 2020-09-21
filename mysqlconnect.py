import mysql.connector

""""In progress -- need to add mysql library"""

cnx = mysql.connector.connect(user='root', password='password',host='127.0.0.1',database='employees', use_pure=False)
cnx.close()