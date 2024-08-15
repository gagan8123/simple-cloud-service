import sqlite3

conn = sqlite3.connect("django_database.db")
while 1:
    q = input("enter query: ")
    print(conn.execute(q).fetchall())
    conn.commit()
