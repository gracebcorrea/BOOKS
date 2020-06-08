import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import os

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

startTime = datetime.datetime.now()

print ( f"starting actions at: {startTime}")

#  ======= Creating tables
#books table
db.execute(""" CREATE TABLE books (
    id SERIAL NOT NULL,
    isbn varchar(100) NOT NULL,
    title varchar (100) NOT NULL,
    author varchar(100) NOT NULL,
    year integer NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (isbn) )  """)
print('books table created')

# users table
db.execute(""" CREATE TABLE users (
    name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (email));  """)

print('users table created')
# reviews table
db.execute(""" CREATE TABLE reviews (
    email varchar(100) NOT NULL,
    rating integer NOT NULL,
    comment varchar(1200) NOT NULL,
    isbn varchar(100) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE) ;  """)

print('reviews table created')

f = open('books.csv')
reader = csv.reader(f)


i = 1
endtime = None
for isbn, title, author, year in reader:

    i += 1
    endtime = datetime.datetime.now()

    if title == 'title':
        print (' Skipping 1st row')
    else:
        db.execute(" INSERT INTO public.books (isbn, title, author, year ) VALUES (:a, :b, :c, :d)", {'a':isbn, 'b':title, 'c': author, 'd':year} )
        print ( f"{i} books added successfully at {endtime}")

# for name, email password in reader2:

db.commit()
timeDiff = endtime - startTime
timeDiffSeconds = timeDiff.seconds
print ( f"Total time to complete action: {timeDiff} ")
print ( f"Total time to complete action in seconds: {timeDiffSeconds} ")
