import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

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
file_dir = os.path.join(script_dir,'movie-database.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{file_dir}"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(255), nullable=True)
    img_url: Mapped[str] = mapped_column(String(255), nullable=False)


with app.app_context():
    db.create_all()

# add first movie
# movie = Movie(
#     title = "Phone Booth",
#     year = 2002,
#     description = "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's " \
#                     "sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads " \
#                     "to a jaw-dropping climax.",
#     rating = 7.5,
#     ranking = 10,
#     review = "My favourite character was the caller.",
#     img_url = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# movie = Movie(
#     title = "Avatar The Way of Water",
#     year = 2022,
#     description = "Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating = 7.3,
#     ranking = 9,
#     review = "I liked the water.",
#     img_url = "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )

# with app.app_context():
#     db.session.add(movie)
#     db.session.commit()


@app.route("/")
def home():
    with app.app_context():
        movies = db.session.execute(db.select(Movie).order_by(Movie.ranking)).scalars().all()

        return render_template("index.html", all_movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
