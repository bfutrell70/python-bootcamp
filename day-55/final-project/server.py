import random
from flask import Flask
app = Flask(__name__)

TOO_LOW_URL = "https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"
TOO_HIGH_URL = "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"
CORRECT_URL = "https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"

number_to_guess = random.randint(0, 9)
print(number_to_guess)

# def header_message_decorator(function):
#     def wrapper(*args):
#         print(args[0])
#         header_markup = ''
#         if args[0] > number_to_guess:
#             header_markup = "<h1 style='color: purple'>Too high, try again!</h1>"
#         elif args[0] < number_to_guess:
#             header_markup = "<h1 style='color: red'>Too low, try again!</h1>"
#         else:
#             header_markup = "<h1 style='color: green'>You found me!</h1>"
#         result = function(args[0])
#         return header_markup + result
#     return wrapper
#
# def image_decorator(function):
#     def wrapper(*args):
#         image_url = ""
#         if args[0] > number_to_guess:
#             image_url = TOO_HIGH_URL
#         elif args[0] < number_to_guess:
#             image_url = TOO_LOW_URL
#         else:
#             image_url = CORRECT_URL
#         image_element = f"<img src='{image_url}'>"
#         return image_element + function(*args)
#     return wrapper

@app.route("/")
def home_page():
    return ("<h1 style='text-align: center'>Guess a number between 0 and 9</h1>"
            "<img style='text-align: center' src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'>")

@app.route("/<int:guess>")
# @image_decorator
def guess_number(guess):
    image_url = ''
    header_markup = ''
    if guess == number_to_guess:
        image_url = CORRECT_URL
        header_markup = f"<h1 style='color: green'>You found me!</h1>"
    elif guess > number_to_guess:
        image_url = TOO_HIGH_URL
        header_markup = f"<h1 style='color: purple'>Too high, try again!</h1>"
    else:
        image_url = TOO_LOW_URL
        header_markup = f"<h1 style='color: red'>Too low, try again!</h1>"

    return header_markup + f"<img src='{image_url}'>"


# if this file is run as a script perform a task
if __name__ == "__main__":
    app.run(debug=True)