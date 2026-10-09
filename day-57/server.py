import datetime

from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def home():
    random_number = random.randint(1,10)
    year = datetime.datetime.now().year
    return render_template("index.html", random_number=random_number, year=year)

if __name__ == "__main__":
    app.run(debug=True)