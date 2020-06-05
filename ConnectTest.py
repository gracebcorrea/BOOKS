import os
import db



#connect to db
con = db.connect(
    host = "ec2-34-198-243-120.compute-1.amazonaws.com",
    database = "d3ck6mm9jbc163",
    user = "dgssjhgflgvwxj",
    password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740",
    )

#cursor
cur = con.cursor()

print ("Hello World")
#execute query
cur.execute("SELECT id, name from ConnectTest")

print ("I´m connected")
rows = cur.fechall()

for row in rows:
  print (f"id {row[0]} name {row[1]}")


#close cursor
cur.close()
#close connection
con.close()
