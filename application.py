import os, requests, sqlalchemy, json, psycopg2, login
from flask import Flask, session, render_template, request, redirect, url_for , jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key= "project1"

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

username = ""

@app.route("/index")
@app.route("/")
def index():
    if session.get('user') is None:
        return render_template("index.html", Search="F", Bookspage="F", Login="T", NewUser="T" ,logout="F" )
    else:
        username=session['user']
        return render_template("index.html", Search="T", Bookspage="F", Login="F", NewUser="F", Logout="T", username=username )


# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       username = request.form.get("username")
       password = request.form.get("password")
       #check if the user exists on the base
       if db.execute("SELECT * FROM users WHERE username = :username and password = :password", {"username": username, "password": password}).rowcount == 1:
           #abrir seçao
           session['user']=username
           print(f"sessao iniciada login:" , [username] )
           return render_template("search.html",Search="T", Bookspage="F", Login="F", NewUser="F", Logout="T", username=username )
       else:
           return render_template("Alerts.html",tipo="alert alert-primary", message="This User or E-mail is not valid, please try again or join us", username=username , NewUrl="/index")

    else:
         return render_template("login.html")


#create new user
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form.get("username")
       password = request.form.get("password")
       ckpassword = request.form.get("checkpassword")

       #check if the user exists on the base
       if db.execute("SELECT * FROM users WHERE username = :username",
                     {"username": username}).fetchone():
            return render_template("Alerts.html",tipo="alert alert-danger", message="This User is not new, try again or go to login page, ", username=username , NewUrl="/index")

       elif password != ckpassword:
            return render_template("Alerts.html",tipo="alert alert-danger", message="Passwords do no check, please try again, ", username=username , NewUrl="/register")
            session.clear()
       else:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)" , { "username" : username, "password": password } )
            db.commit()
            session['user']= username

            print(f"Usuário registrado:" , [username] )
            return render_template("Alerts.html",tipo="alert alert-success", message="You joined us with sucess:", username=session['user'], NewUrl="/search")
    else:
        return render_template("register.html")



@app.route("/search", methods=['GET', 'POST'])
def search():
    if session.get('user') is None:
        return render_template("Alerts.html", tipo="alert alert-danger", message="You are not logged, please login or join us",  NewUrl="/login")

    if request.method == "POST":
        username = session['user']
        print(f"sessao search:" , [username])
        SQLquerry = "%"+request.form.get("SQLquerry")+"%"
        results = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn OR title LIKE :title OR author LIKE :author OR year LIKE :year)", {"isbn":SQLquerry, "title":SQLquerry, "author":SQLquerry, "year":SQLquerry}).fetchall()
        if len(results):
            return render_template("search.html", results=results , Search="T", Bookspage="F", Login="F", NewUser="F", Logout="T", username=username)
        else:
            return render_template("Alerts.html", tipo="alert alert-danger", message="404 Not Found - This ISBN  is not in Database",  NewUrl="/search")
    else:
        username = session['user']
        return render_template("search.html", Search="T", Bookspage="F", Login="F", NewUser="F", Logout="T", username=username )




# Review Page

@app.route("/bookspage", methods=["GET", "POST"])
#def bookspage():
#    return("bookspage.html")
@app.route("/bookspage/<ISBN>", methods=["GET", "POST"])
def bookspage(ISBN):
    if session.get('user') is None:
           return render_template("Alerts.html",tipo="alert alert-danger", message="You are not logged, please login", NewUrl="/login")

    username=session['user']
    myISBN=ISBN
    print("sessao bookspage:" , [ISBN],[username] )
    #Getting book query from database
    book = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn)", {"isbn": myISBN}).fetchone()
    #Getting Goodreads API data:"
    goodreads=[]
    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": myISBN})

    #Check if API is working
    #return(goodreads.json())
    #fields exemple
    # { "books": [ {
    #"average_rating": "4.42",
    #"id": 25494343,
    #"isbn": "1442468351",
    #"isbn13": "9781442468351",
    #"ratings_count": 137430,
    #"reviews_count": 370450,
    #"text_reviews_count": 14395,
    #"work_ratings_count": 155150,
    #"work_reviews_count": 405313,
    #"work_text_reviews_count": 17119 }]
    #}

    API_Av_Rating =""
    API_id = ""
    API_isbn= ""
    API_ratings_count =""
    API_reviews_count = ""
    try:
       goodreads = goodreads.json()
       goodreads = goodreads["books"][0]
       API_Av_Rating = goodreads["average_rating"]
       API_id = goodreads["id"]
       API_isbn= goodreads["isbn"]
       API_ratings_count =goodreads["ratings_count"]
       API_reviews_count = goodreads["reviews_count"]

    except ValueError:
        print(f"Response content is not valid JSON")


    #Getting Review query for the book
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": myISBN}).fetchall()
    if len(reviews):
        return render_template("bookspage.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T",
                                  book=book, reviews=reviews, isbn=API_isbn, ratings_count = API_ratings_count,
                                  reviews_count=API_reviews_count, average_rating=API_Av_Rating , username=username)

        print("sessao bookspage" , [ISBN],[username], [API_reviews_count],[API_reviews_count] )
    else:
        return render_template("bookspage.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T",
                                      book=book, isbn=API_isbn, ratings_count = API_ratings_count, reviews_count=API_reviews_count,
                                       average_rating=API_Av_Rating , username=username, msgrev = "No reviews for this book")


        #Treat the new review and rating



        if request.method == "POST":
            username = session['user']
            myISBN=API_isbn
            Newreview=request.form.get("Newreview")
            rating=request.form.get("rating")
            print("Inside  POST" ,[username] , [API_isbn], [Newreview],[rating])


                #Saving / updating a new review:
            MyReview  = db.execute("SELECT username FROM reviews WHERE username = :username AND isbn = :isbn",
                          {"username": username, "isbn": API_isbn}).fetchone()

            if len(MyReview):
                print("Trying to UPDATE:"   [Newreview], [rating] , [myISBN],[ username])

                try:
                    db.execute("UPDATE reviews SET review = :review, rating = :rating WHERE username = :username AND isbn = :isbn",
                          {"review": Newreview, "rating": rating, "username": username, "isbn": API_isbn})
                    db.commit()
                    return render_template("Alerts.html", tipo="alert alert-sucess", message="Review Updated, Thank You!" , username = username, NewUrl="search")
                except:
                    return render_template("Alerts.html", tipo="alert alert-danger", message="Something worng with UPDATE, please ty again" , username = username,NewUrl="bookspage")
            else:
                print("Trying to SAVE:"  , [Newreview], [rating] , [myISBN],[ username])
                try:
                    db.execute("INSERT INTO reviews ( isbn, review , rating, username, rating, ) VALUES (:isbn, :review, :rating, :username)",
                         {"isbn": API_isbn, "review": Newreview , "rating": rating, "username": username})
                    db.commit()
                    return render_template("Alerts.html", tipo="alert alert-sucess", message="New Review Saved, Thank You!" , username = username, NewUrl="search")
                except:
                    return render_template("Alerts.html", tipo="alert alert-danger", message="Something wrong with INSERT, please ty again" , username = username,NewUrl="bookspage" )


        return render_template("bookspage.html", Search="T", Bookspage="T", Login="F", NewUser="F", Logout="T",
                              book=book, reviews=reviews, isbn=API_isbn, ratings_count = API_ratings_count,
                              reviews_count=API_reviews_count, average_rating=API_Av_Rating , username=username, msgrev ="No reviews to show")






#check sessions
@app.route('/user')
def user():
    if 'user' in session:
        username = session['user']
        return f"<h1>username<h1>"
    else:
        return redirect(url_for('login'))


#Logout: Logged in users should be able to log out of the site.
@app.route('/logout')
def logout():
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
#    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
#                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": ISBN})
#    return(goodreads.json())


#@app.route("/goodreads")
#def goodreads():
#    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
#                        params={"key": "vELE3rrO4BMGthbgfBiKA", "isbns": "9781632168146"})
#    return(goodreads.json())
