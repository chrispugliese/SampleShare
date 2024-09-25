import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    # you password maybe different so enter the password you setup on mysql
    password = 'YourMom!73'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE sampleshare")

print("All Done!")