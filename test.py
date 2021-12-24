import sqlite3

db =sqlite3.connect("botSellFile.bak")
cur = db.cursor()
cur.execute("select * from users")
x = cur.fetchall()
for i in x:
    print(i)

