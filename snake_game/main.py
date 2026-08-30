from turtle import Screen
import time

from food import Food
from snake import Snake
from scoreboard import ScoreBoard

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = ScoreBoard()

# set up key listeners
screen.listen()
screen.onkey(fun=snake.up, key="Up")
screen.onkey(fun=snake.down, key="Down")
screen.onkey(fun=snake.left, key="Left")
screen.onkey(fun=snake.right, key="Right")


game_is_on = True

while game_is_on:
    # moved out of the for loop to make it appear that the entire snake is moving at once
    screen.update()
    time.sleep(0.1)

    snake.move()

    # detect collision with food
    # turtle.distance()
    if snake.head.distance(food) < 15:
        print("nom nom nom")
        scoreboard.increment_score()
        food.refresh()
        snake.extend()

    # detect collision with wall
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 \
        or snake.head.ycor() > 280 or snake.head.ycor() < -280:
        game_is_on = False
        scoreboard.game_over()

    # detect collision with tail
    # if head collides with any segment in the tail game over
    # for segment in snake.segments:
    # using slicing to exclude the first element, which is also head
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()

# last line of code
screen.exitonclick()
