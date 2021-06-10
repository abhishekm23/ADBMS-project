import psycopg2


name=input("Enter name:")
age=int(input("Enter age:"))
gender=input("Enter gender:")

conn=psycopg2.connect("dbname=sample1 user=postgres password=qw3rtyui0p")
cur=conn.cursor()
cur.execute("INSERT INTO sample_data VALUES (%s,%s,%s)",(name,age,gender))
conn.commit()
cur.close()
conn.close()