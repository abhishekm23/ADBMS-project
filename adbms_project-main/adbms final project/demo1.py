import psycopg2
from references import db_password


name=input("Enter name:")
age=input("Enter age:")

conn=psycopg2.connect("dbname=sample1 user=postgres password={}".format(db_password))
curr=conn.cursor()
curr.execute("INSERT INTO sample_data_7 VALUES('{}','{}')".format(name,age))
conn.commit()
curr.close()
conn.close()
