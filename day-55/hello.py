from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
def say_bye():
    return "<p>Bye, World!</p>"

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"<p>Hello there, {name}, you are {number} years old!</p>"

# if this file is run as a script perform a task
if __name__ == "__main__":
    app.run(debug=True)