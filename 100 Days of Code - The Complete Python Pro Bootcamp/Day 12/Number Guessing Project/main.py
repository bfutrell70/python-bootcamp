import random
import art

EASY_GUESSES = 10
HARD_GUESSES = 5

"""
Ask user to select difficulty level
'easy' - 10 guesses
'hard' - 5 guesses

set max_guesses based on selected difficulty
randomly choose a number between 1 and 100

while max_guesses is not 0 and the random number has not been guessed
    ask user to enter a guess

    check if the guess is equal to the random number
        inform the user they guessed the number correctly
    else if the guess is lower than the random number
        inform the user that the number is too low and to guess again
        subtract 1 from max_guesses
    else
        inform the user that the number is too high and to guess again
        subtract 1 from max_guesses
"""

def check_guess(guess, computer_number):
    """
    checks if the user's guess matches the number to guess or not
    :param guess: user's guess
    :param computer_number: number user is trying to guess
    :return: True if the user guessed correctly, False if not
    """
    if guess == computer_number:
        print(f"\tYou got it! The answer was {computer_number}!")
        return True
    elif guess < computer_number:
        print(f"\tYour guess was too low.")
    else:
        print("\tYour guess was too high.")

    return False

def get_user_input(user_prompt, valid_responses):
    """
    Get input from the user, making them enter until a valid response is given
    :param user_prompt: prompt to show to the user
    :param valid_responses: a list of strings containing valid responses
    :return: a valid response from the user
    """
    response = ""
    while response not in valid_responses:
        response = input(user_prompt).lower()
        if response not in valid_responses:
            print(f"\t'{response}' is not a valid response. Please try again.")

    return response

def get_user_guess(remaining_guesses):
    """
    Get the user's guess for the random number
    :return: int containing the user's guess
    """
    print(f"You have {remaining_guesses} attempts remaining to guess the number")
    return int(input("Please enter your guess: "))

def deduct_from_number_of_guesses(remaining_guesses):
    new_guesses = remaining_guesses - 1
    return new_guesses

def get_difficulty_level():
    """
    ask the user to select a difficulty level
    :return: int representing the number of guesses based on the difficulty level
    """
    difficulty = get_user_input(
        user_prompt="Please select a difficulty level. Type 'easy' or 'hard': ",
        valid_responses= ['easy','hard'])

    if difficulty == "easy":
        return EASY_GUESSES
    else:
        return HARD_GUESSES

def get_random_number():
    return random.randint(1, 100)

print(art.logo)
print("Welcome to the number guessing game!")
print("I'm thinking of a number between 1 and 100.")

# global variables
guesses = get_difficulty_level()
number_to_guess = get_random_number()
user_guess = 0
continue_game = True

# game logic
while guesses != 0 and continue_game:
    user_guess = get_user_guess(guesses)
    if check_guess(user_guess, number_to_guess):
        continue_game = False
    else:
        guesses = deduct_from_number_of_guesses(guesses)

        if guesses == 0:
            print("You've run out of guesses, you lose.")
        else:
            print("\tGuess again.")
