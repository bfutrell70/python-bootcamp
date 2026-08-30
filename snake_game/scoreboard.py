from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Arial", 12, "normal")

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 280)
        self.display_score()

    def increment_score(self):
        self.score += 1
        self.display_score()

    def display_score(self):
        self.clear()
        self.write(
            arg=f"Score: {self.score}",
            move=False,
            align=ALIGNMENT,
            font=FONT)

    def game_over(self):
        self.setposition(0,0)
        self.write(
            arg=f"GAME OVER",
            move=False,
            align=ALIGNMENT,
            font=FONT)
