import psycopg2

#connect db
db = psycopg2.connect(
      host = "ec2-34-198-243-120.compute-1.amazonaws.com",
      database= "d3ck6mm9jbc163",
      user = "dgssjhgflgvwxj",
      password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740")

#cursor
cur = db.cursor()

#execute query see all tables on the db
#cur.execute( "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER By table_name;")
#Tables = cur.fetchall()
#for T in Tables:
    #print([T])


cur.execute("SELECT * FROM ConnectTest WHERE Schema = 'public' ORDER By name ;")
Rows = cur.fetchall()
for r in Rows:
   print (f"id {r[0]}, name {[1]}")


#close cursor
cur.close()

#close connection
db.close()
