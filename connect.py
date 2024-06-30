import mysql.connector


def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="<Your_Username>",
        passwd="<Your_Password>",
        database="<Your_Database_Name>",
        auth_plugin='mysql_native_password'
    )
    return mydb

