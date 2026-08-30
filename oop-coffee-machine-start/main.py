from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

coffee_menu = Menu()
making_money_machine = MoneyMachine()
coffee_maker_machine = CoffeeMaker()

coffee_machine_off = False

# run as long as the coffee machine is on
while not coffee_machine_off:
    choice = input(f"What would you like? ({coffee_menu.get_items()}): ").lower()

    if choice == "report":
        # print reports - not displayed to the user
        coffee_maker_machine.report()
        making_money_machine.report()
    elif choice == "off":
        # turn off the coffee machine - not displayed to the user
        coffee_machine_off = True
        print("Powering down...")
    else:
        # user picked a drink
        selected_drink = coffee_menu.find_drink(choice)

        # only proceed if the user's drink was found
        if selected_drink is not None:
            # check if the drink can be made given the resources available
            sufficient_resources = coffee_maker_machine.is_resource_sufficient(selected_drink)

            if sufficient_resources:
                # ask the user to enter the quantity of each type of coin and determine
                # if they have paid enough for their drink
                money_paid = making_money_machine.make_payment(selected_drink.cost)

                if money_paid:
                    # make the drink and deduct the resources the drink used
                    coffee_maker_machine.make_coffee(selected_drink)
