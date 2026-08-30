from turtle import Turtle

FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("black")
        self.hideturtle()
        self.level = 1

    def increase_level(self):
        self.level += 1
        self.write_level()

    def write_level(self):
        self.clear()
        self.goto(-280, 260)
        self.write(f"Level: {self.level}", font=FONT, align="left")

    def write_game_over(self):
        # self.clear()
        self.goto(0,0)
        self.write(arg="GAME OVER", align="center", font=FONT)
