import p1db

#connect to db
con = p1db.connect({
    host ="ec2-34-198-243-120.compute-1.amazonaws.com",
    database="d3ck6mm9jbc163",
    user="dgssjhgflgvwxj",
    password="b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740",
    })
#cursor
cur = con.cursor()



#close connection
con.close()
