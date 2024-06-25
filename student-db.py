import mysql.connector


database = mysql.connector.connect(
    host = 'localhost',
    username = 'root',
    passwd = 'Amey1234'
)

cursorObject = database.cursor()


cursorObject.execute('CREATE DATABASE campus_connect')

print("Database Connected")