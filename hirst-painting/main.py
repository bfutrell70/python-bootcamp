from turtle import Screen, Turtle
from random import Random

color_list = [
    (202, 164, 110), (240, 245, 241), (236, 239, 243), (149, 75, 50), (222, 201, 136),
    (53, 93, 123), (170, 154, 41), (138, 31, 20), (134, 163, 184), (197, 92, 73),
    (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70), (232, 176, 165),
    (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74),
    (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102), (12, 70, 64),
    (107, 127, 153), (176, 192, 208), (168, 99, 102)
]

# requirements
# 10 x 10 rows of spots
# should be about 20 in space, with 50 between dots
random = Random()
art = Turtle()
screen = Screen()
screen.colormode(255)
art.speed("fastest")
SPACING = 50

def random_color():
    return random.choice(color_list)

def draw_circle(x_position, y_position):
    art.penup()
    art.setx(x_position)
    art.sety(y_position)
    #print(f"circle x: {x_position}, y: {y_position}")
    art.pendown()

    color = random_color()
    # could also use .dot(), which creates a filled circle
    art.fillcolor(color)
    art.color(color)
    art.begin_fill()
    art.circle(10)
    art.end_fill()

def draw_row(y_position):
    x_position = -200
    for _ in range(10):
        draw_circle(x_position, y_position)
        x_position += SPACING

# get Turtle window size to calculate where the turtle should start drawing
# spacing of 50
# 9 spacings between the first and last circle
total_width = SPACING * 9
y = -200

for i in range(10):
    draw_row(y)
    y += SPACING

art.hideturtle()
screen.exitonclick()