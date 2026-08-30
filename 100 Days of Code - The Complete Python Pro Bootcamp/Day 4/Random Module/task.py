import random
# import my_module

# print(random.randint(1, 10))
# print(my_module.my_favorite_number)

# print(random.random() * 100)
# generates a random float between 0 and 1 excluding 1
# random_number_between_0_and_1 = random.random() * 10
# print(random_number_between_0_and_1)

# generates a random float between the two values
# includes both values
# random_float = random.uniform(1,10)
# print(random_float)

heads_or_tails = random.randint(0, 1)
if heads_or_tails == 0:
    print("Heads")
else:
    print("Tails")