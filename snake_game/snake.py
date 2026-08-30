from turtle import Turtle

LOCATIONS = [(0,0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
START_X = 0
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:
    def __init__(self):
        self.segments = []
        self.initialize_segments()
        # for ease of referring to the first list item in code
        self.head = self.segments[0]

    def initialize_segments(self):
        """
        sets up the initial state of the snake
        with three segments with the first starting at (0,0)
        and the other two to the left of it
        """
        # x_coordinate = START_X
        for index in range(3):
            self.add_segment(LOCATIONS[index])
            # new_turtle = Turtle(shape="square")
            # new_turtle.color("white")
            # new_turtle.penup()
            # new_turtle.setx(x_coordinate)
            # self.segments.append(new_turtle)
            #
            # x_coordinate -= 20

    def move(self):
        """
        moves the snake by setting a segment's position in the list
        to the segment with the next lowest index in the list
        """
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)

        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def add_segment(self, position):
        new_turtle = Turtle(shape="square")
        new_turtle.color("white")
        new_turtle.penup()
        new_turtle.setposition(position)
        self.segments.append(new_turtle)

    def extend(self):
        """ add a segment to the snake"""
        self.add_segment(self.segments[-1].position())
