import random

friends = ["Alice", "Bob", "Charlie", "David", "Emanuel"]

number_of_friends = len(friends)

# picks a random integer and gets the element from the list
print(friends[random.randint(0, number_of_friends - 1)])

# choice picks a random item from the list
print(random.choice(friends))