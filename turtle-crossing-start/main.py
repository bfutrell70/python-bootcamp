import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

"""
1. A turtle moves forwards when you press the "Up" key. It can only move forwards, not back, left or right.

2. Cars are randomly generated along the y-axis and will move from the right edge of the screen to the left edge.

3. When the turtle hits the top edge of the screen, it moves back to the original position and the player levels up. 
    On the next level, the car speed increases.

4. When the turtle collides with a car, it's game over and everything stops.
"""

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.colormode(255)

player = Player()
manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(player.move, "Up")

game_is_on = True
# counter = 1
scoreboard.write_level()

def check_for_collision():
    """
    checks if there was a collision between the turtle and a car
    returns True if there was a collision, False if not.
    """
    for car in manager.cars:
        # thinking of using these to implement a more precise collision detection method
        x = player.xcor()
        y = player.ycor()
        car_x = car.xcor()
        car_y = car.ycor()

        if player.distance(car) < 20:
            return True

    return False

while game_is_on:
    time.sleep(0.1)
    screen.update()

    # determine if a new car should be added to the screen
    # counter += 1
    # if counter == 6:
    manager.add_car()
    # counter = 1

    manager.move_cars()
    manager.cleanup_cars()

    if check_for_collision():
        game_is_on = False
        scoreboard.write_game_over()

    if player.is_on_top_of_screen():
        scoreboard.increase_level()
        player.reset()
        manager.increase_speed()


screen.exitonclick()