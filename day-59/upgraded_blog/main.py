import datetime
import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template
import random

# NOTE: this URL is blocked by the firewall on the company's WiFi network.
#       Try with the iPhone's hotspot.
API_URL = 'https://api.npoint.io/bd0e107f49d63fdb1643'
blog_posts = requests.get(API_URL).json()

app = Flask(__name__)



@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", blog_posts=blog_posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    post = [p for p in blog_posts if p['id'] == post_id][0]

    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)