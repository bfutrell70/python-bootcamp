from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()
DISTANCE = 10
ANGLE = 10

def move_forwards():
    tim.forward(DISTANCE)

def move_backwards():
    tim.backward(DISTANCE)

def turn_left():
    current_heading = tim.heading()
    # tim.setheading(current_heading - ANGLE)
    # can also use tim.left(<number of degrees>)
    tim.left(ANGLE)

def turn_right():
    current_heading = tim.heading()
    # tim.setheading(current_heading + ANGLE)
    # can also use tim.right(<number of degrees>)
    tim.right(ANGLE)

def clear_drawing():
    # tim.clear()
    # tim.home()
    tim.reset()

# w - forwards
# s - backwards
# a - counter-clockwise
# d - clockwise
# c - clear drawing

screen.listen()
screen.onkey(key="w", fun=move_forwards)
screen.onkey(key="s", fun=move_backwards)
screen.onkey(key="a", fun=turn_left)
screen.onkey(key="d", fun=turn_right)
screen.onkey(key="c", fun=clear_drawing)




screen.exitonclick()