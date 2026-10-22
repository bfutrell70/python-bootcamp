import os

import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
file_dir = os.path.join(script_dir,'instance','cafes.db')
# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{file_dir}'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# I had previously named this function 'random', which overrode Python's
# built-in random library.
@app.route('/random', methods=["GET"])
def random_cafe():
    with app.app_context():
        result = db.session.execute(db.select(Cafe))
        all_cafes = result.scalars().all()
        cafe = random.choice(all_cafes)
        # all_cafes: list[Cafe] = Cafe.query.all()
        # cafe = random.choice(all_cafes)
        # --- all of the above into a single line ---
        # cafe = random.choice(Cafe.query.all())
        return jsonify(cafe={
            "can_take_calls":cafe.can_take_calls,
            "coffee_price":cafe.coffee_price,
            "has_sockets":cafe.has_sockets,
            "has_toilet":cafe.has_toilet,
            "has_wifi":cafe.has_wifi,
            "id":cafe.id,
            "img_url":cafe.img_url,
            "location":cafe.location,
            "map_url":cafe.map_url,
            "name":cafe.name,
            "seats":cafe.seats
            }
        )


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
