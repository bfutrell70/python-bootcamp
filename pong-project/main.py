from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle()
l_paddle = Paddle(-350, 0)
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(r_paddle.move_up, "Up")
screen.onkey(r_paddle.move_down, "Down")
screen.onkey(l_paddle.move_up, "w")
screen.onkey(l_paddle.move_down, "s")

print(screen.window_height())
print(screen.window_width())

game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    ball.move()

    # check if the ball has hit the top or bottom it will
    # change direction
    if ball.ycor() > 280 or ball.ycor() < -280:
        # needs to bounce
        ball.bounce_y()

    # detect collision with right paddle and left paddle
    if ((ball.distance(r_paddle) < 50 and ball.xcor() > 320) or
            (ball.distance(l_paddle) < 50 and ball.xcor() < - 320)):
        # print("Made contact")
        ball.bounce_x()

    # detect collision with left and right side of the screen
    if ball.xcor() < -380:
        # right player scored a point
        ball.reset_position()
        scoreboard.r_point()

    if ball.xcor() > 380:
        # left player scored a point
        ball.reset_position()
        scoreboard.l_point()

    screen.update()

screen.exitonclick()