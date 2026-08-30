# NOTE - Angela's solution involved recursion (also in solution.py)
# TODO: If the user doesn't want to continue with the previous
#       result, ask if they want to continue running the program.
#       If they don't want to continue running the program, print
#       a goodbye message and exit the program

# TODO: Validate user input for operations and yes / no questions

import art
print(art.logo)

def add(n1, n2):
    return n1 + n2

# TODO 1: write out the other 3 functions - subtract, multiply and divide

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

# TODO 2: Add the 4 functions into a dictionary as the values. Keys = '+', '-', '*', '/'
operators = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}

def check_input(user_input, valid_options):
    """
    Validates that a user's input is within the list of valid options
    :param user_input: text the user entered
    :param valid_options: a list of valid options for the user input
    :return: True if user's input was one of the valid options, False if not.
    """
    if user_input not in valid_options:
        valid_options_text = ",".join(valid_options)
        print(f"Valid options are {valid_options_text}")
        return False

    return True

# TODO 3: Use the dictionary operations to perform the calculations. Multiple 4 * 8
#  using the dictionary.

# print(operators['*'](4, 8))

# --- my code - it works, but doesn't use recursion
# continue_running = True
# use_first_number = True
#
# first_number = 0.0
#
# while continue_running:
#     if use_first_number:
#         first_number = float(input("Type in your first number:\n"))
#
#     operations = ""
#     for op in operators:
#         operations += f"\t{op}\n"
#     math_operation = input(f"Type in your operator:\n{operations}")
#     second_number = float(input("Type in your second number:\n"))
#
#     # perform calculation and show result
#     result = operators[math_operation](first_number, second_number)
#     print(f"{first_number} {math_operation} {second_number} = {result}")
#
#     # Ask if the user wants to perform another operation before asking
#     # if they want to continue using the previous result.
#     # --- NOTE: This was not in the functionality bullet points,
#     # --- but without this there wouldn't be a way to exit the program
#     # --- except to press Ctrl+C to stop execution of the program.
#     more_operations = input("Perform another operation? Enter 'yes' or 'no'.\n").lower()
#     if more_operations == "yes":
#         # Ask if the user wants to continue working with the previous result.
#         # If they do, set the first number to the previous result and
#         # don't ask the user for the first number.
#         use_previous_result = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation.\n").lower()
#         if use_previous_result == "y":
#             first_number = result
#             print(f"Using {first_number} as the first number...")
#             use_first_number = False
#             print("\n\n")
#         else:
#             use_first_number = True
#             print("Clearing results...")
#             print("\n" * 20)
#     else:
#         continue_running = False
#         print("Thank you for using the calculator!")

def calculator():
    should_accumulate = True

    first_number = float(input("Type in your first number:\n"))

    while should_accumulate:
        operations = ""
        for op in operators:
            operations += f"\t{op}\n"

        # give the user a chance to enter a valid operator if they enter
        # an incorrect one
        valid_math_operation = False
        math_operation = ""

        while not valid_math_operation:
            math_operation = input(f"Type in your operator:\n{operations}")
            valid_math_operation = check_input(math_operation, operators)

        second_number = float(input("Type in your second number:\n"))

        # perform calculation and show result
        result = operators[math_operation](first_number, second_number)
        print(f"{first_number} {math_operation} {second_number} = {result}")

        # Ask if the user wants to continue working with the previous result.
        # If they do, set the first number to the previous result and
        # don't ask the user for the first number.
        valid_option = False
        use_previous_result = ""

        while not valid_option:
            use_previous_result = input(f"Type 'y' to continue calculating with {result}, or type 'n' to start a new calculation.\n").lower()
            valid_option = check_input(use_previous_result, ['y', 'n'])

        if use_previous_result == "y":
            first_number = result
        else:
            should_accumulate = False

            # User decided not to continue using the previous result.
            # Ask if they want to keep using the program, and if not
            #   thank them and exit.
            # NOTE: This was not in the functionality list.
            valid_option = False
            exit_program = ""
            while not valid_option:
                exit_program = input("Type 'y' to continue running the program, or 'n' to exit.").lower()
                valid_option = check_input(exit_program, ['y', 'n'])

            if exit_program == 'n':
                print("Thank you for using the calculator!")
            else:
                print("\n" * 20)
                calculator()

calculator()
