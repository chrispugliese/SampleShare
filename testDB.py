import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    # your username maybe different so enter the user name that you entered when you configured mysql
    user="root",
    # your password maybe different so enter the password you setup on mysql
    password="YourMom!73",
)

cursorObject = dataBase.cursor()

cursorObject.execute("INSERT")
