import psycopg2

#connect db
db = psycopg2.connect(
      host = "ec2-34-198-243-120.compute-1.amazonaws.com",
      user = "dgssjhgflgvwxj",
      password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740",
      database= "d3ck6mm9jbc163"      
      )

#cursor
cur = db.cursor()

#execute query see all tables on the db
cur.execute( "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER By table_name;")
Tables = cur.fetchall()
for T in Tables:
    print([T])
    print("Congrats, you accessed the database")

#close cursor
cur.close()

#close connection
db.close()

#connect database on bash
# source venv/Scripts/activate      (ativar ambiente virutal - toda vez que entrar no bash)
# pip install requests    (verifica se tem atualizaçoes)
# flask --version
#set or export FLASK_APP=application.py
#set or export FLASK_DEBUG=1
#set or export DATABASE_URL="postgres://dgssjhgflgvwxj:b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740@ec2-34-198-243-120.compute-1.amazonaws.com:5432/d3ck6mm9jbc163"


#Api Key - Goodreads
#Here is your developer key for using the Goodreads API. This key must be appended to every request using the form variable 'key'. (If you're using our write API, you'll need your secret too.)

#key: vELE3rrO4BMGthbgfBiKA
#secret: fLjGkGg3qi2ftPIlRJJK4gZkKlS8OV1uSnSh89x9Ak
