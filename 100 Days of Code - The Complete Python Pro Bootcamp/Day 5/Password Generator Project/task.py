import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters = int(input("How many letters would you like in your password?\n"))
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

# --- Easy level
# letters, then symbols, then numbers
password = ""

for letter in range(nr_letters):
    # random.choice() is much more readable
    # password += letters[random.randint(0, len(letters) - 1)]
    password += random.choice(letters)

for symbol in range(nr_symbols):
    # password += symbols[random.randint(0, len(symbols) - 1)]
    password += random.choice(symbols)

for number in range(nr_numbers):
    # password += numbers[random.randint(0, len(numbers) - 1)]
    password += random.choice(numbers)

print(f"Easy level password: {password}")

# --- Hard level
# letters, numbers, and symbols can appear in any location
# Same initial code to add the characters to the password string,
# then it will be shuffled with random.shuffle.
# Angela added characters from the three groups to a list named password
#   instead of appending them to a string
#   password += random.choice() is the same as password.append(random.choice())
# Angela used a for loop to add the characters from the list to the password.
chars_to_shuffle = list(password)
random.shuffle(chars_to_shuffle)
password = ''.join(chars_to_shuffle)
print(f"Hard level password: {password}")