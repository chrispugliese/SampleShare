# In case for some reason you need to drop the database this code will delete the database
# Run this code by typing the command "python dropDB.py"

import mysql.connector
from decouple import config
dataBase = mysql.connector.connect(
    host = config("DB_HOST", "db"),
    # your password maybe different so enter the password you setup on mysql
    password = config("MYSQL_PASSWORD")
)

cursorObject = dataBase.cursor()

cursorObject.execute("DROP DATABASE sampleshare_db")

print("Database Successfully Dropped !!")