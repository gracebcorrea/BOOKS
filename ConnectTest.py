import os
import Heroku



#connect to db
con = Heroku.connect(
    host = "ec2-34-198-243-120.compute-1.amazonaws.com",
    database = "d3ck6mm9jbc163",
    user = "dgssjhgflgvwxj",
    password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740",
    )

#cursor
cur = con.cursor()

#execute query
cur.execute("SELECT id, name from ConnectTest")

rows = cur.fechall()
    print("Connected")
    
for r in rows:
    print(f"id {r[0]} ,  name {r[1]})


#close cursor
cur.close()
#close connection
con.close()
