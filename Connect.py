import psycopg2

#connect db
con = psycopg2.connect(
      host = "ec2-34-198-243-120.compute-1.amazonaws.com",
      database= "d3ck6mm9jbc163",
      user = "dgssjhgflgvwxj",
      password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740"
      )
#cursor
cur = con.cursor()

#execute query
cur.execute("select id, name from connecttest")

for r in rows:
    print (f"id {r[0]}, name {[1]}")


#close cursor
cur.close()

#close connection
con.close()
