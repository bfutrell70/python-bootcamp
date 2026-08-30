from turtle import Turtle
from random import Random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10

# cars are randomly generated along the y-axis and will move from the right
# edge of the screen to the left edge
# once the car's position is beyond the left side of the play field,
# remove the car from the list.
class CarManager:
    def __init__(self):
        self.cars = []
        self.move_distance = STARTING_MOVE_DISTANCE

    def add_car(self):
        """ add a car to the list of cars """
        random = Random()

        if random.randint(1, 6) == 1:
            lower_y = -250
            upper_y = 250

            new_car = Turtle("square")
            new_car.penup()
            # new_car.shape("square")
            new_car.setheading(180)
            new_car.shapesize(stretch_len=2)
            new_car.color(random.choice(COLORS))
            new_car.setx(300)
            new_car.sety(random.randrange(lower_y, upper_y, 20))

            self.cars.append(new_car)
            print(f"added a {new_car.pencolor()} car")
            print(f"{len(self.cars)} cars on the screen.")

    def move_cars(self):
        """ moves all cars a set distance """
        for car in self.cars:
            car.forward(self.move_distance)

    def cleanup_cars(self):
        """
        removes cars that have passed the left side of the screen
        from the list of cars
        """

        # starting at the last element in the index to prevent out of range errors
        for i in range(len(self.cars) - 1, -1, -1):
            if self.cars[i].xcor() < -300:
                print(f'\tremoving a {self.cars[i].pencolor()} car.')
                self.cars[i].hideturtle()
                del self.cars[i]
                print(f"{len(self.cars)} remaining.")

    def increase_speed(self):
        self.move_distance += MOVE_INCREMENT
        print(f"increasing speed to {self.move_distance}")