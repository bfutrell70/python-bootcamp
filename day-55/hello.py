from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ("<h1 style='text-align: center'>Hello, World!</h1>"
            "<p>This is a paragraph</p>"
            "<img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjNzeXJyem44MzdobXZlN2JlaG9odGpqaW41OTJzYnZhMjUxaHNzNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OTpjRKwx8q85LEn0in/giphy.gif'>")

@app.route("/bye")
def say_bye():
    return "<p>Bye, World!</p>"

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"<p>Hello there, {name}, you are {number} years old!</p>"

# if this file is run as a script perform a task
if __name__ == "__main__":
    app.run(debug=True)