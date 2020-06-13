import os, requests, sqlalchemy, json, psycopg2, login
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

#connect database on bash
# source venv/Scripts/activate      (ativar ambiente virutal - toda vez que entrar no bash)
# pip install requests    (verifica se tem atualizaçoes)
# flask --version
#set or export FLASK_APP=application.py
#set or export FLASK_DEBUG=1
#set or export DATABASE_URL="postgres://dgssjhgflgvwxj:b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740@ec2-34-198-243-120.compute-1.amazonaws.com:5432/d3ck6mm9jbc163"

#or connect db
#db = psycopg2.connect(
#      host = "ec2-34-198-243-120.compute-1.amazonaws.com",
#      database= "d3ck6mm9jbc163",
#      user = "dgssjhgflgvwxj",
#      password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740")


#cursor
#cur = db.cursor()




# Check for environment variable - begin
if not os.getenv("DATABASE_URL"):
   raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#cursor
#cur = db.cursor()

# Principal Page call
#@app.route("/")
#def index():
#    return render_template("index.html")


@app.route("/index")
@app.route("/")
def index():
    #status = "Loggedout"
    #try:
    #    username=session["username"]
    #    status=""
    #except KeyError:
    #    username=""
    #return render_template("index.html", status=status, username=username)

    return render_template("index.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    print("Entrei no form login")
    if request.method == 'POST':
       username = request.form.get("lusername")
       password = request.form.get("lpassword")
       rememberme = request.form.get("lrememberme")
       print(username, lpassword)

    #check if the user exists on the base
    #if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount >= 1:
       return render_template("Alerts.html",tipo="alert alert-success", message="Wellcome ", username="username" )
    else:
    #    return render_template("Alerts.html",tipo="alert alert-danger" , message="This username or password not on database : " ,  username="username" )
         return render_template("login.html")





@app.route("/register", methods=["GET", "POST"])
def register():
    print("Entrei no form register")
    username = request.form.get("username")
    password = request.form.get("password")
    #check if the user exists on the base
    if db.execute("SELECT * FROM users WHERE username = :username",
                {"username": username}).rowcount > 0:
        return render_template("Alerts.html",username="username", message="This user already exists.")
    else:

        #db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
        #        {"username": username, "password": password})
        #db.commit()
        #session["user_name"] = username #Store user id here
        #session["logged_in"] = True
        #return render_template("search.html")
        return render_template("register.html")



# Search Page
@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")



# Review Page
@app.route("/bookspage", methods=["GET", "POST"])
def bookspage():
    return render_template("bookspage.html")



@app.route('/logout')
def logout():

    # clear user credentials
    session.clear()

    # Redirect user to login form

    return redirect(url_for('login'))
           #close cursor
           #cur.close()


@app.route("/res")
def res():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": "9781632168146"})
    return(res.json())




#close connection
db.close()

if __name__ == "__main__":
    with app.app_context():
        main()
