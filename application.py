import os , requests, sqlalchemy, json
from flask import Flask, session, render_template, request, redirect, url_for,Response,send_from_directory
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)


# Check for environment variable

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
@app.route("/index")
def index():
    return render_template("Index.html", homepage=True)

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    #check if the user exists on the base
    if db.execute("SELECT * FROM users WHERE username = :username",
                {"username": username}).rowcount is none:
        return render_template("Alerts.html", message="This user doesn´t exists, you need to register.")
    else:

    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    #check if the user exists on the base
    if db.execute("SELECT * FROM users WHERE username = :username",
                {"username": username}).rowcount > 0:
        return render_template("Alerts.html", message="This user already exists.")
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
#    session['Logged_user'] = None
#    flash('User not Logged in')
    return redirect(url_for('login'))



@app.route("/res")
def res():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": "9781632168146"})
    return(res.json())


#close cursor
#cur.close()

#close connection
db.close()

if __name__ == "__main__":
    with app.app_context():
        main()
