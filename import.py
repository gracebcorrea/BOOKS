import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


engine= create_engine(os.getenv("DATABASE_URL"))
db =scoped_session(sessionmaker(bind=engine))



def main():
    f = open("books.csv", "r")  # needs to be opened during reading csv
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
               {"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()
        print(f"Added book with ISBN: {isbn} Title: {title}  Author: {author}  Year: {year}")


if __name__ == "__main__":
    main()
