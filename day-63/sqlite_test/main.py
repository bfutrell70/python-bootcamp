import os
# import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

 # Finds the directory where your script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))

# Joins the script directory with your target file name
# file_path = os.path.join(script_dir, "books-collection.db")
# db = sqlite3.connect(file_path)

# cursor = db.cursor()

# create a table in the database
# will throw sqlite3.OperationalError if the table 'books' already exists
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# add data to the table
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")

# commit changes to the database
# db.commit()

# -------------------------------------
# using alchemy to interact with SQLite
# -------------------------------------

"""
Requirements:
    - Create an SQLite database called new-books-collection.db. Remember to initialise the app.
    - Create a table in this database called books.
    - The books table should contain 4 fields: 
        - id, 
        - title, 
        - author and 
        - rating. 
        The fields should have the same limitations as before e.g. INTEGER/FLOAT/VARCHAR/UNIQUE/NOT NULL etc.
    - Provide the Flask "app context" and create the schema in the database.
    - Again, with the flask app context, create a new entry in the books table that consists of the following data:

id: 1

title: "Harry Potter"

author: "J. K. Rowling"

review: 9.3
"""
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

file_dir = os.path.join(script_dir,'new-book-database.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{file_dir}"
db.init_app(app)

# Create the table
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

# create a new book record if there are no record in the book table
with app.app_context():
    books = db.session.execute(db.select(Book))
    if len(books.all()) == 0:
        book = Book(id=1, title='Harry Potter', author='J. K. Rowling', rating=9.3)
        db.session.add(book)
        db.session.commit()

# read all records
with app.app_context():
    # returns a Result object
    result = db.session.execute(db.select(Book).order_by(Book.title))
    # gets the individual elements rather than entire rows
    all_books = result.scalars()

# read a particular record by query
with app.app_context():
    # scalar gets a single element
    book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()

# update a particular record by query
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    book_to_update.title = "Harry Potter and the Chamber of Secrets"
    db.session.commit()

# update a record by primary key
book_id = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_update = db.get_or_04(Book, book_id)
    book_to_update.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()

# delete a particular record by primary key
book_id = 1
with app.app_context():
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    # or book_to_delete = db.get_or_04(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()