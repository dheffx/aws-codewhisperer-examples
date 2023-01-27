"""
Event handler for an AWS Lambda function that will receive an CloudWatch event.
When the event is received a MySQL database should query the notifications table to see if any updates
have been made since the last time this function checked.

The MySQL connection should be established in the global scope for re-use across invocations.
"""

import mysql.connector

MYSQL_HOST = 'localhost'
MYSQL_USER = 'XXXX'
MYSQL_PASSWORD = 'XXXX'

# Connect to MySQL using mysql.connector
mydb = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)


def lambda_handler(event, context):
    """
    Query the notifications table for records that have been created since this lambda last ran
    Return the list of notifications found
    """
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM notifications WHERE processed = 0")
    myresult = cursor.fetchall()
    for x in myresult:
        cursor.execute(
            "UPDATE notifications SET processed = 1 WHERE id = %s", (x[0],))
        mydb.commit()

    return myresult
