# This code will execute a query that will create the database in your local server
# after running this code with "python createDB.py " run the command "python manage.py migrate"

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    # your username maybe different so enter the user name that you entered when you configured mysql
    user = 'root',
    # your password maybe different so enter the password you setup on mysql
    password = 'YourMom!73'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE sampleshare")

print("Database Successfully Created!!")
print("Please run the command 'python manage.py migrate' ")