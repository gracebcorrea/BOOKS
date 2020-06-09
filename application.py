import os
import json
import requests
import sqlalchemy
from flask import Flask, session,render_template,request,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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



# Principal Page call
@app.route("/")
def index():
    return render_template("Index.html", homepage=True)

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Request login
    return render_template("login.html")

    #if request.method == "POST":
    #    email = request.form.get("email")
        # Checking if the user is registered
    #    if db.execute("SELECT id FROM users WHERE email= :email", {"email": email}).fetchone() is not None:
    #        return render_template("login.html", work="Login",
    #                               error_message="The user has already registered. Please Login.")
    #    password = request.form.get("password")
    #    db.execute("INSERT INTO users (email, password) VALUES (:email, :password)",
    #               {"email": email, "password": generate_password_hash(password)})
    #    db.commit()
    #    return render_template("login.html", work="Login", message="Success")

    #return render_template("login.html", work="Login")

@app.route("/Register", methods=["GET", "POST"])
def Register():
    return render_template("Register.html", homepage=True)


# Search Page
@app.route("/search")
def search():
    return render_template("search.html", homepage=True)


# Review Page
@app.route("/bookspage")
def bookspage():
    return render_template("bookspage.html", homepage=True)



@app.route('/logout')
def logout():
    session['Logged_user'] = None
    flash('User not Logged in')
    return redirect(url_for('index'))



@app.route("/res")
def res():
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": "9781632168146"})
    return(res.json())
