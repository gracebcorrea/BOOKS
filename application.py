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


#connect db psycopg2 option
#db = psycopg2.connect(
#      host = "ec2-34-198-243-120.compute-1.amazonaws.com",
#      user = "dgssjhgflgvwxj",
#      password = "b7c2cd60be73f4127ca0dc1159d755dfebcf9881459a8885b2ec2ee4b2cf2740",
#      database= "d3ck6mm9jbc163"
#      )





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
        return render_template("Alerts.html", tipo="alert alert-danger", message="You are not logged, please login or join us", username=username , NewUrl="/index")

    if request.method == "POST":
        session['logged']=True
        SQLquerry = "%"+request.form.get("SQLquerry")+"%"
        results = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn OR title LIKE :title OR author LIKE :author OR year LIKE :year)", {"isbn":SQLquerry, "title":SQLquerry, "author":SQLquerry, "year":SQLquerry}).fetchall()
        return render_template("search.html", results=results , Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T")
        print("sessão register:" ,session['user'], session['logged'])
    else:
        return render_template("search.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T" )




# Review Page


@app.route("/bookspage/<string:ISBN>", methods=['GET', 'POST'])
def bookspage(ISBN):
    if session.get('user') is None:
        session['logged'] =False
        session['user'] = ""
        return render_template("Alerts.html",tipo="alert alert-danger", message="You are not logged, please login", NewUrl="/login")
    else:
        username = session['user']
        session['logged'] = True
        APIres=[]
        ISBN=ISBN
        #Getting Goodreads API data:"
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": ISBN}).json()["books"][0]
        #Check if API is working
        #return(res.json())

        API_Av_Rating = res["average_rating"]
        API_id = res["id"]
        API_isbn= res["isbn"]
        API_isbn13= res["isbn13"]
        API_ratings_count = res["ratings_count"]
        API_reviews_count = res[ "reviews_count"]
        API_text_reviews_count = res["text_reviews_count"]
        API_work_ratings_count = res["work_ratings_count"]
        API_work_reviews_count =res["work_reviews_count"]
        API_work_text_reviews_count = res["work_text_reviews_count"]

        return render_template("bookspage/<string:ISBN>", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T" ,
                ISBN = API_isbn, ratings_count = API_ratings_count, reviews_count=API_reviews_count, average_rating=API_Av_Rating , username=session['user'])



        #Getting Review query
        reviews = db.execute("SELECT * FROM reviews WHERE isbn = :ISBN", {"isbn": ISBN}).fetchall()
        users_review = []
        for review in reviews:
            username= db.execute("SELECT username FROM users WHERE username = :username", {"username": review.username}).fetchone().username
            users_review.append((username, review))

        #Getting books query
        book = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn)", {"isbn":ISBN}).fetchone()
        if book is None:
            return render_template("Alerts.html", tipo="alert alert-danger", message="There is no ISBN with this number. Please  try again.")
        if request.method == "POST":
            username = session['user']
            isbn = ISBN
            ratings_count = request.form.get("ratings_count")
            reviews_count = request.form.get("reviews_count")
            average_rating = request.form.get("average_rating")
            if db.execute("SELECT id FROM reviews WHERE username = :username AND isbn = :ISBN",
                          {"username" :username, "isbn" :ISBN}).fetchone() is None:
                #db.execute(
                #    "INSERT INTO reviews (isbn, review, username, rating) VALUES (:isbn, :review, :username, :rating)",
                #    {"isbn" :ISBN, "review" :review, "username" :username, "rating" :rating})
            #else:
            #    db.execute("UPDATE reviews SET review = :review, rating = :rating WHERE username = :username AND isbn = :ISBN",
            #        {"isbn" :ISBN, "review":review, "username" :username,  "rating" :rating})
            #db.commit()

                return render_template("bookspage.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T" ,
                   book=book, APIres=APIres, users_review=users_review, ratings_count=ratings_count, average_rating=average_rating, username=session['user'])




#Logout: Logged in users should be able to log out of the site.
@app.route('/logout')
def logout():
    session['logged'] = False
    session['user'] = ""
    # clear user credentials
    session.clear()
    #close connection
    db.close()

    # Redirect user to index form
    return redirect(url_for('index'))





if __name__ == "__main__":
    with app.app_context():
        main()


#API original



#@app.route("/res")
#def res():
#    res = requests.get("https://www.goodreads.com/book/review_counts.json",
#                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": ISBN})
#    return(res.json())


#@app.route("/res")
#def res():
#    res = requests.get("https://www.goodreads.com/book/review_counts.json",
#                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": "9781632168146"})
#    return(res.json())
