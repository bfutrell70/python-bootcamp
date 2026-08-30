print("Welcome to Python Pizza Deliveries!")
size = input("What size pizza do you want? S, M or L: ")
pepperoni = input("Do you want pepperoni on your pizza? Y or N: ")
extra_cheese = input("Do you want extra cheese? Y or N: ")

total_price = 0

size = size.lower()
pepperoni = pepperoni.lower()
extra_cheese = extra_cheese.lower()

if size == 's':
    total_price += 15
elif size == 'm':
    total_price += 20
elif size == 'l':
    total_price += 25

if pepperoni == 'y' :
    if size == 's' :
        total_price += 2
    else:
        total_price += 3

if extra_cheese == 'y':
    total_price += 1

print(f"Your final bill is: ${total_price}.")