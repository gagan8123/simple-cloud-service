import sqlite3

# conn = sqlite3.connect("django_database.db")
# cursor = conn.cursor()
# while 1:
#     try:
#         qury = input("enter the query: ")
#         res = cursor.execute(qury).fetchall()
#         print(res)
#         conn.commit()
#     except Exception as e:
#         print("error ",e)
#     print()

import pandas

conn = sqlite3.connect("django_database.db")
while 1:
    query = input("enter the query: ")
    data = conn.execute(query).fetchall()
    conn.commit()
    print(data)



    #login
    #SELECT * FROM sqlite_master WHERE type='table'
    #create table user_login(user_id INTEGER PRIMARY KEY AUTOINCREMENT,user_name varchar(40) not null,user_pass varchar(20) not null); 