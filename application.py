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






#@app.route("/res")
#def res():
#    res = requests.get("https://www.goodreads.com/book/review_counts.json",
#                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": "9781632168146"})
#    return(res.json())
