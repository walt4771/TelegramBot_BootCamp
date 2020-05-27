import sqlite3

dbConn = sqlite3.connect('Book.db')
dbCur = dbConn.cursor()

table_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='MESSAGE'"
table_create = 'CREATE TABLE BOOK(' \
                       'ID INTEGER PRIMARY KEY AUTOINCREMENT, CONTENT TEXT, DATE TEXT)'
if not dbCur.execute(table_exists).fetchone():
    dbCur.execute(table_create)

f = open('Book.txt', mode='r', encoding='utf-8')
DATE = "2020/06/00"
data = ""

while True:
    line = str(f.readline())
    if not line:
        break
    data += line
f.close()

length = 2000
data = map(''.join, zip(*[iter(data)]*length))

data = list(data)
i = len(data)

for j in range(0, i):
    query = "INSERT INTO BOOK (CONTENT, DATE) VALUES('{}', '{}')".format(data[j], DATE)
    print(query)
    dbCur.execute(query)

dbConn.commit()
dbConn.close()
