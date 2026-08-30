from idlelib.format import reformat_comment
from turtle import Turtle
from random import Random

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        random = Random()
        # generates locations that a segment would be in
        # random_x = random.randint(-280, 280)
        # random_y = random.randint(-280, 280)
        random_x = random.randrange(-280, 280, 20)
        random_y = random.randrange(-280, 280, 20)
        self.goto(random_x, random_y)