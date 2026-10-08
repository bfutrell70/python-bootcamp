from flask import Flask

# __name__ and __main__ are special attributes built into Python
# __name__ is the current class function name

# @app.route() is a Python decorator
# gives a function specific behavior

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
def say_bye():
    return "<p>Bye, World!</p>"

# if this file is run as a script perform a task
if __name__ == "__main__":
    app.run(debug=True)