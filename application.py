import os , requests, sqlalchemy, json, imgkit, codecs
from flask import Flask, session, render_template, request, redirect, url_for,Response,send_from_directory
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from PIL import Image


app = Flask(__name__)

STATIC_URL = '/static/'
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

        return render_template("login.html")
    #return render_template("login.html", work="Login")

    # Get form information.
#    username = request.form.get("username")
#    password = request.form.get("password")

    # Make sure the login exists.
#    try:
#        login_cred = db.execute("SELECT username, password FROM users WHERE username = :username", {"username" : username}).fetchone()
#        hash = pbkdf2_sha256.verify(password, login_cred.password)

#        if hash is True and username == login_cred.username:
#            session["user_name"] = username #Store user id here
#            session["logged_in"] = True
#            return render_template("search.html")
#        else:
#            return render_template("error.html", message="Wrong username and/or password!")
#    except AttributeError:
#        return render_template("error.html", message="Wrong username and/or password!")
#    except ValueError:
#        return render_template("error.html", message="Wrong username and/or password!")



@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if db.execute("SELECT * FROM users WHERE username = :username",
                {"username": username}).rowcount > 0:
        return render_template("error.html", message="This user already exists.")
    #else:
    #    password1 = pbkdf2_sha256.hash(password)
        # password2 = sha256_crypt.encrypt(password1)

    #    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
    #            {"username": username, "password": password1})
    #    db.commit()
    #    session["user_name"] = username #Store user id here
    #    session["logged_in"] = True
    #    return render_template("search.html")

    return render_template("register.html")


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


#close cursor
#cur.close()

#close connection
db.close()

if __name__ == "__main__":
    with app.app_context():
        main()
