from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280

# player can only move forward when the Up key is pressed
class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.color("green")
        self.setposition(STARTING_POSITION)
        self.setheading(90)

    def move(self):
        """ moves the turtle forward """
        y_position = self.ycor()
        y_position += MOVE_DISTANCE

        print(f"y_position: {y_position}")

        self.goto(self.xcor(), y_position)

    def is_on_top_of_screen(self):
        """ checks if the turtle reached the top of the screen """
        y_position = self.ycor()
        return y_position > FINISH_LINE_Y

    def reset(self):
        self.clear()
        self.goto(STARTING_POSITION)
