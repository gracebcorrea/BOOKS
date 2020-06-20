# Project 1

Web Programming with Python and JavaScript

The goal of this project is to show the knowledge acquired in lectures 2,3 and 4, obeying the rules stipulated for graduation of the project1.

0)File Testcon.py
  I created this file just to build enovironment and check connection with database.
  passwords for use database and what to set in bash are on this file.

1) File createtables.py
   Creates the necessary tables to meet the project:
   users
   Books
   reviews

2) File import.py
    imports the "books.csv" file provided in the project specification

3) Index.html
   Shows the cover page with options to login or create a new user - IT is the Homepage

4) layout.html
    Grants that all pages have the same style and menu format

5) Login.html
      Allows the user to enter the site, if all is ok redirect to search page
      if something go wrong display error messages from Alerts.html using parameters

6) register.html
      Allows the user to registrate on site, if all is right redirect to serach pages
      if something go wrong display error messages from Alerts.html using parameters

7) Logout
      If the user logout dislplay message and redirect do Home or index.html

8) Search.html
      After login user can search a book from the database and list research results

9) Bookspage.html
      After search the book and click on the books ISBN redirect to this page and Shows
      details from the book, also allow to make a review on the book.
