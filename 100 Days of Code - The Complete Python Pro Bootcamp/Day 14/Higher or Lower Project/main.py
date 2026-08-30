import art
import random
from game_data import data

def select_person():
    return random.choice(data)

def check_guess(person_1, person_2, guess):
    """
    checks the user's guess
    :param person_1: first person shown
    :param person_2: second person shown
    :param guess: user's guess
    :return: True if the user was correct, false if not
    """
    # determine what the correct guess should be based on follower count
    if person_1['follower_count'] > person_2['follower_count']:
        correct_guess = "A"
    else:
        correct_guess = "B"

    # compare user's guess against the correct answer
    guess = guess.upper()
    if guess == correct_guess:
        return True

    return False

def display_people(person_1, person_2, last_guess_correct = False, score = 0):
    """
    displays the randomly selected people in a standard format
    :param person_1: first person to display
    :param person_2: second person to display
    :param last_guess_correct: True if the last guess the user made was correct
    :param score: player's score
    """
    print(art.logo)
    if last_guess_correct:
        print(f"You're right! Current score: {score}")
    display_person(person=person_1, letter='A')
    print(art.vs)
    display_person(person=person_2, letter='B')


def display_person(person, letter):
    """
    Displays a person in a human-readable format
    :param person: person to display
    :param letter: 'A' or 'B'
    """
    first_word = "Compare"
    if letter.lower() == 'b':
        first_word = "Against"

    name = person['name']
    description = person['description']
    country = person['country']

    print(f"{first_word} {letter.upper()}, {name}, a {description}, from {country}.")

def display_end_of_game(score):
    """
    displays the end of game with the final score
    :return:
    """
    print("\n" * 20)
    print(art.logo)
    print(f"Sorry, that's wrong. Final score: {score}")

def game():
    """
    Plays the game
    """
    player_score = 0
    continue_game = True
    previous_guess_correct = False

    # making the second person match the first one to
    # force the second person to be selected at random
    first_person = select_person()
    second_person = first_person

    while continue_game:
        while second_person == first_person:
            second_person = select_person()

        display_people(
            person_1=first_person,
            person_2=second_person,
            last_guess_correct=previous_guess_correct,
            score=player_score)

        user_guess = input("Who has more followers? Type 'A' or 'B': ").upper()

        guess_correct = check_guess(
            person_1=first_person,
            person_2=second_person,
            guess=user_guess)

        if guess_correct:
            player_score += 1
            previous_guess_correct=True
            first_person = second_person
        else:
            display_end_of_game(player_score)
            continue_game = False

game()