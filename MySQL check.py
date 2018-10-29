import mysql.connector
import os
from SlackMessage import messageToSlack
import getpass

'''
The function connects to the MySQL database using the credentials entered by the user,
runs a scan on all the tables in the database, if any table is nearing the MAX Auto-Increment value,
it sends a messsage to a Slack Team workspace with the name of the table, so that the issue can be resolved.
The Slack channel the message needs to be sent to can be edited according to the user.
'''

def checkMySQLtables(user_name, password, host, db_name):
    try:
        con= mysql.connector.connect(user=user_name, password=password,
                                 host=host,
                                 database=db_name)
        cursor=con.cursor()
        cursor.execute(" SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='demodb'; ")
        
        for row in cursor.fetchall():
            cursor.execute("SELECT LAST_INSERT_ID() from {} group by last_insert_id();".format(row[0]))
            result=cursor.fetchall()
            if result[0]>4294960000:   #4294967625 being the MAX value
                message="Auto-Increment ID reaching max value in table "+row[0]+", Please take required action!"
                channel="general"         #can be changed according to need
                messageToSlack(message, channel)
            
    except mysql.connector.errors.DatabaseError:
        print("couldnt connect to database, recheck credentials!")
        

if __name__=="__main__":
    print("enter database credentials.")
    user_name=input("enter name of user: ")
    password=getpass.getpass()
    host=input("enter host adress: ")
    db_name=input("enter Database Name: ")

    checkMySQLtables(user_name, password, host, db_name)
