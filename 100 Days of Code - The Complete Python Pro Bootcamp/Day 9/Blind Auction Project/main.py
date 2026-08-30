import art

bidders = {}

# display art and welcome message
print(art.logo)
print("Welcome to the silent auction program! \n")

def clear_screen():
    print("\n" * 100)

# TODO-4: Compare bids in dictionary
def find_highest_bid(list_of_bids):
    winning_name = ""
    winning_bid = 0

    # instead of looping through the items in a dictionary, we can use Python's max() function
    # to get the key associated with the highest value
    winning_name = max(list_of_bids, key=list_of_bids.get)
    winning_bid = list_of_bids[winning_name]

    # looping through list of keys
    # for bidder in list_of_bids:
    #     if list_of_bids[bidder] > winning_bid:
    #         winning_name = bidder
    #         winning_bid = list_of_bids[bidder]

    print(f"The winner is {winning_name} with a bid of ${"{:.2f}".format(winning_bid)}")

add_bidders = True

while add_bidders:
    # TODO-1: Ask the user for input
    name = input("What is your name? ")
    bid = float(input("What is your bid?: $ "))

    # TODO-2: Save data into dictionary {name: price}
    bidders[name] = bid

    # TODO-3: Whether if new bids need to be added
    more_bidders = input("Are there any other bidders? Type 'yes' or 'no'.\n").lower()
    if more_bidders == 'no':
        add_bidders = False
    else:
        clear_screen()

find_highest_bid(bidders)