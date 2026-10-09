from flask import Flask
from markupsafe import escape

app = Flask(__name__)

# START DECORATOR FUNCTIONS
def make_bold(function):
    def wrapper_function():
        result = function()
        return f"<b>{result}</b>"

    return wrapper_function


def make_emphasis(function):
    def wrapper_function():
        result = function()
        return f"<em>{result}</em>"

    return wrapper_function


def make_underlined(function):
    def wrapper_function():
        result = function()
        return f"<u>{result}</u>"

    return wrapper_function
# END DECORATOR FUNCTIONS

@app.route("/")
def hello_world():
    return ("<h1 style='text-align: center'>Hello, World!</h1>"
            "<p>This is a paragraph</p>"
            "<img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjNzeXJyem44MzdobXZlN2JlaG9odGpqaW41OTJzYnZhMjUxaHNzNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OTpjRKwx8q85LEn0in/giphy.gif'>")

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "<p>Bye, World!</p>"

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"<p>Hello there, {name}, you are {number} years old!</p>"

# if this file is run as a script perform a task
if __name__ == "__main__":
    app.run(debug=True)