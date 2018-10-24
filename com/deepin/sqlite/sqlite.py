import sqlite3

conn = sqlite3.connect('C:/sqlite/test.db')
c = conn.cursor()
print("Opened database successfully")
# cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
cursor = c.execute("SELECT * from COMPANY WHERE name='{}'".format("Paul"))
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")

print("Operation done successfully")
conn.close()
