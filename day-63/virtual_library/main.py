import os
import re

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from wtforms import StringField, IntegerField, SubmitField, FloatField, HiddenField
from wtforms.validators import DataRequired

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


# Finds the directory where your script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))


class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

file_dir = os.path.join(script_dir,'new-book-database.db')
app = Flask(__name__)
app.secret_key = "kjsdflkjmrx0932uix,heimdj"
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

# -------- START CRUD functions ---------
def get_all_books():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
        return result


def get_book(book_id):
    with app.app_context():
        return db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()


def add_book(book:Book):
    with app.app_context():
        db.session.add(book)
        db.session.commit()

def update_rating(book_id:int, rating:float):
    with app.app_context():
        book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        if book_to_update:
            book_to_update.rating = rating
            db.session.commit()

def delete_book(book_id):
    with app.app_context():
        book = db.get_or_404(Book, book_id)
        db.session.delete(book)
        db.session.commit()

# -------- END CRUD functions ---------

# -------- START Routes --------------
@app.route('/')
def home():
    global all_books
    all_books = get_all_books()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    global all_books
    if request.method == "POST":
        book_name = request.form.get('book_name') or ""
        author = request.form.get('author') or ""
        rating = request.form.get('rating') or 0

        book_to_add = Book()
        book_to_add.title = book_name
        book_to_add.author = author
        book_to_add.rating = float(rating)

        # must confirm that the book title doesn't exist before saving it


        add_book(book_to_add)

        # print(all_books)
        # all_books = get_all_books()

        return redirect(url_for('home'))
    
    return render_template("add.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form['id']
        rating = request.form['rating']
        update_rating(book_id=book_id, rating=rating)
        return redirect(url_for('home'))

    book_id = request.args.get('id')
    book = get_book(book_id)
    return render_template("edit.html", book=book)

@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    delete_book(book_id)
    return redirect(url_for('home'))

# -------- END Routes --------------

# --------------------------------------------


all_books = get_all_books()



if __name__ == "__main__":
    app.run(debug=True)

