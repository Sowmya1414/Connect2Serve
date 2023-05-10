#to create a database using mysql


import mysql.connector

#database connection of user_db
db1 = mysql.connector.connect(
    host='localhost',
    user='root',
    password='hello',
    
)
db_cursor=db1.cursor()
#db_cursor.execute("CREATE DATABASE connect2serve_db_1")





db_cursor.execute('SHOW DATABASES')
for db in db_cursor:
    print(db)