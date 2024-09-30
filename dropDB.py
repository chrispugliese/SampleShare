# In case for some reason you need to drop the database this code will delete the database
# Run this code by typing the command "python dropDB.py"

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    # your username maybe different so enter the user name that you entered when you configured mysql
    user = 'root',
    # you password maybe different so enter the password you setup on mysql
    password = 'password123'
)

cursorObject = dataBase.cursor()

cursorObject.execute("DROP DATABASE sampleshare")

print("Database Successfully Dropped !!")