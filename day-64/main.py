import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
from api_functions import APIFunctions
from MovieData import MovieData

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

movie_search_api = "https://api.themoviedb.org/3/search/movie"
image_url = "https://image.tmdb.org/t/p/original"
load_dotenv()
api_read_token = os.environ['API_READ_ACCESS_TOKEN']

api_functions = APIFunctions()
movie_search_results: list[MovieData] = []

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


class MovieForm(FlaskForm):
    id = HiddenField('id', validators=[DataRequired()])
    rating = FloatField('Your Rating Out of 10 (e.g. 7.5)')
    review = StringField('Your Review')
    submit = SubmitField('Done')

class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.rating))
        movies = result.scalars().all()

        # assign rankings
        for i in range(len(movies)):
            movies[i].ranking = len(movies) - i
        db.session.commit()

        return render_template("index.html", all_movies=movies)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = MovieForm()
    if form.validate_on_submit():
        # FORM POST
        movie_id = form.id.data
        if movie_id:
            movie_id = int(movie_id)
        else:
            movie_id = 0

        with app.app_context():
            movie = db.get_or_404(Movie, movie_id)
            # movie = db.session.execute(db.select(Movie).where(Movie.id == form.id.data)).scalar()

            movie.rating = form.rating.data
            movie.review = form.review.data

            db.session.commit()
            return redirect(url_for('home'))
    
    id = request.args.get('id')

    with app.app_context():
        movie = db.get_or_404(Movie, id)
        form = MovieForm()
        form.id.data = str(movie.id)
        form.rating.data = movie.rating
        form.review.data = movie.review

    return render_template("edit.html", form=form, movie=movie)

@app.route('/delete/<int:id>')
def delete(id):
    with app.app_context():
        movie = db.get_or_404(Movie, id)
        db.session.delete(movie)
        db.session.commit()

    return redirect(url_for('home'))

@app.route("/add", methods=["GET","POST"])
def add():
    global movie_search_results
    form = AddMovieForm()

    if form.validate_on_submit():
        movie_search_results = api_functions.search_for_movies(search_text=form.title.data)

        return redirect(url_for('select'))

    return render_template("add.html", form=form)

@app.route("/select")
def select():
    movie_id = int(request.args.get('id', -1))
    if movie_id != -1:
        movie_to_add:MovieData = movie_search_results[movie_id]
        print(movie_to_add.__dict__)

        # add the movie to the database, then go to the home page.
        with app.app_context():
            m = Movie(
                title = movie_to_add.title,
                img_url = movie_to_add.img_url,
                year = int(movie_to_add.year[:4]),
                description = movie_to_add.description
            )
            db.session.add(m)
            db.session.commit()

            print(m.__dict__)
            print(m.id)

            # return redirect(url_for('home'))
            return redirect(url_for('edit', id=m.id))

    return render_template("select.html", movies=movie_search_results)


"""
Requirement 4
1 - [DONE] define a WTForm with a single field for the title of a movie
2 - when Add Movie is clicked the server should receive the movie title
    a) make a request to The Movie Database API to find movies that match the title.
        - should the movie match the user title or contain the user title?
        - https://api.themoviedb.org/3/search/movie?query=<<movie title>>
    b) pass the results from the API to the select.html page
3 - once the user selects a movie from the select.html page:
    a) make an API call to the details API
        - https://api.themoviedb.org/3/movie/<<movie id>>
        - get the following properties and save them to the database:
            - title             (title)
            - img_url           (poster_path) - doesn't appear to be a full URL
            - year              (release_date (full date - just get the year))
            - description       (overview)

            ** img_url is only the image filename
            ** full URL is https://image.tmdb.org/t/p/<<size>>/<<img_url value>>
            ** https://image.tmdb.org/t/p/original/hbhFnRzzg6ZDmm8YAmxBnQpQIPh.jpg
4 - once data is saved to the database, redirect to edit.html
    a) this allows the user to assign a rating and add a review
        

"""


if __name__ == '__main__':
    app.run(debug=True)
