import os, requests, sqlalchemy, json, psycopg2, login
from flask import Flask, session, render_template, request, redirect, url_for , jsonify
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


#connect db
db = psycopg2.connect(
      host = "ec2-34-198-243-120.compute-1.amazonaws.com",
      user = "dgssjhgflgvwxj",
      password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740",
      database= "d3ck6mm9jbc163"
      )





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


@app.route("/index")
@app.route("/")
def index():
    if session.get('user') is None:
        session['user'] = []
        session['logged']= []
        return render_template("index.html", Search="F", Bookspage="F", Login="T", NewUser="T" ,logout="F" )

    else:
        request.method == 'POST'
        username= request.form.get("username")
        session['user'].append(username)
        session['logged'].append(True)
        return render_template("index.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T" )


# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
       username = request.form.get("username")
       password = request.form.get("password")
       rememberme = request.form.get("rememberme")

       #check if the user exists on the base
       if db.execute("SELECT * FROM users WHERE username = :username and password = :password", {"username": username, "password": password}).rowcount == 1:
           #abrir seçao
           session['user'].append(username)
           session['logged'].append(True)
           print("sessão iniciada:" , session['user'], session['logged'])
           return render_template("search.html",Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T", username=username )
       else:
           return render_template("Alerts.html",tipo="alert alert-primary", message="This User or E-mail is not valid, please try again or join us", username=username , NewUrl="/index")
           session['logged'] = False

    else:
         return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form.get("username")
       password = request.form.get("password")
       ckpassword = request.form.get("checkpassword")

       #check if the user exists on the base
       if db.execute("SELECT * FROM users WHERE username = :username",
                     {"username": username}).fetchone():
            #print("user exists")
            return render_template("Alerts.html",tipo="alert alert-danger", message="This User is not new, try again or go to login page, ", username=username , NewUrl="/index")

       elif password != ckpassword:

            return render_template("Alerts.html",tipo="alert alert-danger", message="Passwords do no check, please try again, ", username=username , NewUrl="/register")
            session.clear()
       else:

            #db.execute(SQL,USERDATA)
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)" , { "username" : username, "password": password } )
            db.commit()

            session['user'].append(username)
            session['logged'].append(True)
            print("sessão register:" ,session['user'], session['logged'])
            return render_template("Alerts.html",tipo="alert alert-success", message="You joined us with sucess:", username=session['user'], NewUrl="/search")
    else:
        return render_template("register.html")



@app.route("/search", methods=['GET', 'POST'])
def search():
    if session.get('user') is None:
        session['logged'] =False
        session['user']= ""
        return render_template("Alerts.html", tipo="alert alert-danger", message="You are not logged, please login or join us", username=username , NewUrl="/index")

    if request.method == "POST":
        SQLquerry = "%"+request.form.get("SQLquerry")+"%"
        results = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn OR title LIKE :title OR author LIKE :author OR year LIKE :year)", {"isbn":SQLquerry, "title":SQLquerry, "author":SQLquerry, "year":SQLquerry}).fetchall()
        return render_template("SQLresults.html", results=results)

    else:
        return render_template("search.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T" )



# Review Page
@app.route("/bookspage", methods=['GET', 'POST'])
def bookspage():
    if session.get('user') is None:
        return render_template("Alerts.html",tipo="alert alert-danger", message="You are not logged, please login", username=session['user'], NewUrl="/index")
    else:
        return render_template("bookspage.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T" , username=session['user'])



#Logout: Logged in users should be able to log out of the site.
@app.route('/logout')
def logout():
    session['logged'] = False
    # clear user credentials
    session.clear()
    #close connection
    db.close()

    # Redirect user to index form
    return redirect(url_for('index'))


@app.route("/res")
def res():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": "vELE3rrO4BMGthbgfBiKA", "ISBMs": "9781632168146"})
    return(res.json())


if __name__ == "__main__":
    with app.app_context():
        main()
