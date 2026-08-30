from turtle import Turtle

PADDLE_INCREMENT = 20
LENGTH_STRETCH = 1
WIDTH_STRETCH = 5
INITIAL_X = 350
INITIAL_Y = 0

class Paddle(Turtle):
    def __init__(self, x = INITIAL_X, y=INITIAL_Y):
        """
        Initializes the Paddle class
        :param x: starting x position (defaults to INITIAL_X if not set)
        :param y: starting y position (defaults to INITIAL_Y if not set)
        """
        super().__init__()
        self.x = x
        self.y = y
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_wid=WIDTH_STRETCH, stretch_len=LENGTH_STRETCH)
        self.penup()
        self.goto(x, y)

    def move_up(self):
        self.y = self.ycor() + PADDLE_INCREMENT
        self.goto(self.xcor(), self.y)

    def move_down(self):
        self.y = self.ycor() - PADDLE_INCREMENT
        self.goto(self.xcor(), self.y)