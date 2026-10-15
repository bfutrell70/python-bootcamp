import smtplib
import ssl
from email.message import EmailMessage
from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv


# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get('https://api.npoint.io/c790b4d5cab58020d391').json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        load_dotenv()

        my_email = os.environ['EMAIL_ADDRESS']
        password = os.environ['PASSWORD']
        
        form_data = request.form
        print("-------------------------")
        print(f"name: {form_data["name"]}")
        print(f"email: {form_data["email"]}")
        print(f"phone: {form_data["phone"]}")
        print(f"message: {form_data["message"]}")
        print("-------------------------")

        msg = EmailMessage()
        msg['Subject'] = "New Message From Day 60"
        msg["From"] = form_data['email']
        msg["To"] = my_email
        msg.set_content(f"Phone: {form_data['phone']}\n\n{form_data['message']}")

        smtp_server = 'smtp.gmail.com'
        # port = 465      # standard port for SSL
        port = 587      # standard port for TLS

        with smtplib.SMTP(smtp_server, port) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.send_message(msg)
    return render_template("contact.html", request_method=request.method)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
