# *args - unlimited arguments - similar to params in C#
def add(*args):
    total = 0

    # an option to get the total of args - looping
    # for n in args:
    #     total += n

    # another option to get the total of args - using sum()
    total = sum(args)
    return total

print(add(2, 4, 5, 6, 7))

# **kwargs - many named keyword arguments
def calculate(n, **kwargs):
    print(kwargs)
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)

    # can refer to value of a name by referring it to a key
    # print(kwargs["add"])

    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)

calculate(2, add=3, multiply=5)

class Car:
    def __init__(self, **kw):
        # get() returns None if the key doesn't exist
        # if kw["key"] doesn't exist an error will occur
        self.make = kw.get("make")
        self.model = kw.get("model")

my_car = Car(make="Oldsmobile")
print(my_car.make)
print(my_car.model)