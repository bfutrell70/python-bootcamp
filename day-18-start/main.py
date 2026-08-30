from turtle import Turtle, Screen
from random import Random

random = Random()
tim = Turtle()
screen = Screen()
screen.colormode(255)
tim.speed("fastest")

# timmy_turtle.shape("turtle")
# timmy_turtle.color("purple4")

# Turtle Challenge 1 - Draw a Square
# for _ in range(4):
#     tim.forward(100)
#     tim.right(90)

# Turtle Challenge 2 - Draw a Dashed Line
# for _ in range(50):
#     tim.pendown()
#     tim.forward(4)
#     tim.penup()
#     tim.forward(4)

# Turtle Challenge 3 - Drawing Different Shapes
# draw a triangle, square, pentagon, hexagon, heptagon, octagon, nonagon, decagon
# sides of each shape are 100
# each shape is drawn in a random color
# def draw_shape(number_of_sides):
#     angle_degrees = 360 / number_of_sides
#     for _ in range(number_of_sides):
#         tim.right(angle_degrees)
#         tim.forward(100)
#
#
def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue
#
#
# # for sides in [3, 4, 5, 6, 7, 8, 9, 10]:
# for sides in range(3, 11):
#     tim.pencolor(generate_random_color())
#     draw_shape(sides)

# Turtle Challenge 4 - Generate a Random Walk
# random number of degrees at 90 degree intervals
# random color for each segment
# thickness of line is thicker than normal
# see about speeding up the drawing

def generate_random_direction():
    return random.choice([0, 90, 180, 270])

# tim.pensize(7)
# tim.speed("fastest")
# for _ in range(250):
#     tim.setheading(generate_random_direction())
#     tim.pencolor(generate_random_color())
#
#     if random.choices([True, False]):
#         tim.forward(20)
#     else:
#         tim.backward(20)

# Turtle Challenge 5 - Draw a Spirograph
# circle radius of 100
def draw_circle():
    tim.circle(100)

def spirograph(number_of_circles):
    tim.pensize(3)
    angle = int(360 / number_of_circles)
    for _ in range(number_of_circles):
        tim.right(angle)
        tim.color(generate_random_color())
        draw_circle()

spirograph(72)

# keep on bottom
screen.exitonclick()