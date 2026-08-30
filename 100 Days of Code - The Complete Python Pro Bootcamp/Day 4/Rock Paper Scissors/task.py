import random
import sys

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

options = [rock, paper, scissors]

# rules
# - [0] rock wins against [2] scissors
# - [1] paper wins against [0] rock
# - [2] scissors wins against [1] paper
# all other combinations are losing combinations

# ask user to enter 0 for rock, 1 for paper, or 2 for scissors
# randomly pick an item in the list for the computer
# compare user's selection against computer's selection
# if the selections don't fit one of the three rules the user lost

player_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n"))
computer_choice = random.randint(0, len(options) - 1)

player_wins = False
tie_game = False

if player_choice < 0 or player_choice > 2:
    # invalid user selection
    print("You typed an invalid number - you lose!")
    sys.exit()
elif player_choice == computer_choice:
    # player and computer chose the same option, which is a draw
    tie_game = True
else:
    if player_choice == 0 and computer_choice == 2:
        # rock beats scissors
        player_wins = True
    elif player_choice == 1 and computer_choice == 0:
        # paper beats rock
        player_wins = True
    elif player_choice == 2 and computer_choice == 1:
        # scissors beats paper
        player_wins = True
    else:
        # other combinations of rock-paper-scissors results in a loss
        player_wins = False

print(options[player_choice])
print("Computer chose:")
print(options[computer_choice])

if tie_game:
    print("Tied game!")
else:
    if player_wins:
        print("You win!")
    else:
        print("You lose!")