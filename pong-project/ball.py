from turtle import Turtle

MOVE_DISTANCE = 10

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0,0)
        self.speed(1)
        self.move_x = MOVE_DISTANCE
        self.move_y = MOVE_DISTANCE
        self.move_speed = 0.1

    def move(self):
        new_x = self.xcor() + self.move_x
        new_y = self.ycor() + self.move_y
        self.setx(new_x)
        self.sety(new_y)

        # Angela had this in main.py
        # makes sense when you factor in paddle collision checking.
        # # if the y coordinate is about to reach the top or bottom,
        # # change the direction of movement on the y axis
        # if self.ycor() > 290 or self.ycor() < -290:
        #     self.move_y = -self.move_y

    def bounce_y(self):
        self.move_y *= -1

    def bounce_x(self):
        self.move_x *= -1
        # gradually reduces the delay between movements
        self.move_speed *= 0.9

    def reset_position(self):
        self.goto(0,0)
        self.bounce_x()
        # reset the move speed
        self.move_speed = 0.1