from random import Random
from turtle import Turtle, Screen

is_race_on = False

random = Random()
screen = Screen()
screen.setup(width=500,height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

turtles = []

START_X = -230
END_X = 230
START_Y = -110

def initialize_turtles():
    y = START_Y
    # set color and call penup() for each turtle
    for index in range(6):
        new_turtle = Turtle(shape="turtle")
        new_turtle.color(colors[index])
        new_turtle.penup()
        new_turtle.goto(START_X, y)
        turtles.append(new_turtle)
        y += 50

# tim.penup()
# tim.goto(x=-230, y=-100)

initialize_turtles()

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in turtles:
        if turtle.xcor() > END_X:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")
        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)

screen.exitonclick()