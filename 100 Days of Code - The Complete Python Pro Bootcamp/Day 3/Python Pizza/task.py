import sys

print("Welcome to Python Pizza Deliveries!")
size = input("What size pizza do you want? S, M or L: ")
pepperoni = input("Do you want pepperoni on your pizza? Y or N: ")
extra_cheese = input("Do you want extra cheese? Y or N: ")

price = 0

# determine initial price of pizza based on size
if size == "S":
    price = 15
elif size == "M":
    price = 20
elif size == "L":
    price = 25
else:
    print("Invalid size selection - exiting program!")
    sys.exit()

# determine additional cost for pepperoni
if pepperoni == "Y":
    if size == "S":
        price += 2
    else:
        price += 3

# determine additional cost for cheese
if extra_cheese == "Y":
    price += 1

print(f"Your final bill is: ${price}.")
