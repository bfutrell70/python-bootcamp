age = -1

while age == -1:
    try:
        age = int(input("How old are you? "))
    except ValueError:
        print("A string is not a valid input. Please enter a number. ")

if age > 18:
    print(f"You can drive at age {age}.")
