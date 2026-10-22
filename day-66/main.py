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

    # --- the code below would build a list of columns and return a dictionary
    def to_dict(self):
    #     #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
    #     #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
    #     return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")



# HTTP GET - Read Record

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

        # return jsonify(cafe={
        #     "can_take_calls":cafe.can_take_calls,
        #     "coffee_price":cafe.coffee_price,
        #     "has_sockets":cafe.has_sockets,
        #     "has_toilet":cafe.has_toilet,
        #     "has_wifi":cafe.has_wifi,
        #     "id":cafe.id,
        #     "img_url":cafe.img_url,
        #     "location":cafe.location,
        #     "map_url":cafe.map_url,
        #     "name":cafe.name,
        #     "seats":cafe.seats
        #     }
        # )
        return jsonify(cafe=cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    all_cafes = Cafe.query.all()

    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def search():
    loc = request.args.get("loc")
    # if not loc:
    #     loc = ""
    with app.app_context():
        # in a where clause searching for strings is case sensitive
        results = db.session.execute(db.select(Cafe).where(Cafe.location == loc)).scalars().all()
        if len(results) == 0:
            return jsonify(error={
                "Not Found": "Sorry, we don't have a cafe at that location."
            })
        else:
            return jsonify(cafes=[cafe.to_dict() for cafe in results])

# HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_cafe():
    data = request.get_json()
    cafe = Cafe(
        name=data.get("name"),
        can_take_calls=data.get("can_take_calls"),
        coffee_price=data.get("coffee_price"),
        has_sockets=data.get("has_sockets"),
        has_toilet=data.get("has_toilet"),
        has_wifi=data.get("has_wifi"),
        # id=request.form.get("id"),
        img_url=data.get("img_url"),
        location=data.get("location"),
        map_url=data.get("map_url"),
        seats=data.get("seats"),
    )

    with app.app_context():
        db.session.add(cafe)
        db.session.commit()

        return jsonify(response = {"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
