import datetime
import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template
import random

app = Flask(__name__)

load_dotenv()
API_KEY = os.environ['AGIFY_API_KEY']

@app.route("/")
def home():
    random_number = random.randint(1,10)
    year = datetime.datetime.now().year
    return render_template("index.html", random_number=random_number, year=year)

@app.route("/guess/<name>")
def guess(name):
    name = name.title()

    agify_url = f"https://api.agify.io/?name={name}&apikey={API_KEY}"
    genderize_url = f"https://api.genderize.io/?name={name}&apikey={API_KEY}"

    agify_response = requests.get(agify_url)
    genderize_response = requests.get(genderize_url)

    gender = genderize_response.json()["gender"]
    age = agify_response.json()["age"]

    return render_template("guess.html", name=name, gender=gender, age=age)

if __name__ == "__main__":
    app.run(debug=True)