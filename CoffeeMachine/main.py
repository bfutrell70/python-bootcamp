MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    },
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

# global variables
ESPRESSO = "espresso"
LATTE = "latte"
CAPPUCCINO = "cappuccino"
OFF = "off"
REPORT = "report"

total_funds = 0.00
drink_info = {}

# ------------------ Functions --------------------


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


def get_number(user_prompt):
    """
    get a valid number from the user
    :param user_prompt: message to display to the user
    :return: an int
    """
    valid_number = False
    value = 0
    while not valid_number:
        try:
            value = int(input(user_prompt))
            valid_number = True
        except ValueError:
            print("\tPlease input a valid number.")

    return value


def print_report():
    print("Machine resources report")
    print("------------------------")
    print(f"\tWater: {resources['water']}ml")
    print(f"\tMilk: {resources['milk']}ml")
    print(f"\tCoffee: {resources['coffee']}ml")
    print(f"\tMoney: ${total_funds:.2f}\n")


def calculate_total_funds():
    """
    calculate the total funds provided by the user based on the
    number of quarters, dimes, nickels, and pennies
    :return: total cash amount of the coins entered by the user
    """
    quarters = get_number("Enter the number of quarters: ")
    dimes = get_number("Enter the number of dimes: ")
    nickels = get_number("Enter the number of nickels: ")
    pennies = get_number("Enter the number of pennies: ")

    payment = pennies * 0.01
    payment += nickels * 0.05
    payment += dimes * 0.10
    payment += quarters * 0.25

    return payment


def check_resources():
    """
    check if the machine has enough resources to make a drink
    :return: True if there are enough resources to make the user's drink, False if not
    """
    enough_resources = True

    # -- based on Angela's code --
    # Since the ingredients for the drink are iterated through it doesn't require
    # checking that a key exists since only keys the drink's ingredients contains
    # will be used.
    #
    # Her code checks to see if the resource from the drink is equal to or greater than
    # the resources of the coffee machine. To me if the machine has the same amonut of a
    # resource then the drink can be made.
    for ingredient in drink_info["ingredients"]:
        if drink_info["ingredients"][ingredient] > resources[ingredient]:
            print(f"Sorry, there is not enough {ingredient}.")
            enough_resources = False

    return enough_resources


def make_drink(machine_resources):
    """
    make the user's selected drink
    :param machine_resources: the remaining resources the machine has
    :return: an updated dictionary of resources
    """

    for ingredient in drink_info["ingredients"]:
        machine_resources[ingredient] -= drink_info["ingredients"][ingredient]

    return machine_resources


def process_purchase(payment):
    """
    determines if the user paid enough for their drink
    :param payment: amount the user paid
    :return: True if the user paid enough for their drink, False if not
    """
    # from Angela's solution
    global total_funds

    cost_of_drink = drink_info["cost"]
    if payment < cost_of_drink:
        print("Sorry that's not enough money. Money refunded.")
        return False
    else:
        # from Angela's solution - I had this in the main logic
        total_funds += cost_of_drink
        if total_payment > drink_cost:
            change = total_payment - drink_cost
            print(f"Here is ${change:.2f} in change")
        return True


# -------------------------- Main Logic -------------------------
enough_funds = False
resources_available = False
continue_running = True

while continue_running:
    # TODO 1: prompt user by asking "What would you like? (espresso/latte/cappuccino): "
    valid_options = ["espresso", "latte", "cappuccino", "off", "report"]
    selected_drink = get_user_input(
        user_prompt="What would you like? (espresso/latte/cappuccino): ",
        valid_responses=valid_options,
    )

    # TODO 2: turn off the Coffee Machine by entering "off" to the prompt
    if selected_drink == OFF:
        continue_running = False

    # TODO 3: print report of resources and money by entering "report" to the prompt
    elif selected_drink == REPORT:
        print_report()

    # TODO 4: check if there are enough resources to create the users' drink
    #       if there isn't enough of a resource, display "Sorry there is not enough <resource>
    else:
        drink_info = MENU[selected_drink]
        resources_available = check_resources()

        if resources_available:
            # TODO 5: process coins
            #       - if there are enough resources to create the selected drink, prompt the user to insert coins
            #       - prompt for number of quarters, dimes, nickels, and pennies
            #       - calculate the total value of the coins
            total_payment = calculate_total_funds()

            # TODO 6: check if transaction is successful
            #       - if the user didn't provide enough coins to pay for the drink, inform the user
            #       that "Sorry that's not enough money. Money refunded."
            #       - if the user provided enough money to cover the drink, add the cost of the drink
            #       to the machine
            #       - if the user entered too much money, the machine should offer change
            #       "Here is $2.45 dollars in change", with change rounded to 2 decimal places
            drink_cost = drink_info["cost"]
            enough_funds = process_purchase(payment=total_payment)
            # if enough_funds:
            #     if total_payment > drink_cost:
            #         change = total_payment - drink_cost
            #         print(f"Here is ${change:.2f} in change")
            #     total_funds += drink_cost

        # TODO 7: make coffee
        #       - if there are enough resources to make coffee and the user supplied enough money to pay
        #       for the drink, the resources to make the drink should be deducted from the coffee machine
        #       resources
        #       - once the resources have been deducted, tell the user
        #       "Here is your <selected drink>. Enjoy"
        if resources_available and enough_funds:
            resources = make_drink(machine_resources=resources)
            print(f"Here is your {selected_drink}. Enjoy! ☕")
