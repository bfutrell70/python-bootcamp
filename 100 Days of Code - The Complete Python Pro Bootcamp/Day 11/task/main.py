import random
import art

def clear_screen():
    print("\n" * 30)

def calculate_score(hand):
    """
    calculates the score for a set of cards
    :param hand: a list of cards for the player or dealer
    :return: total score of the cards
    """
    score = sum(hand)
    ace = 11

    # check if the total score is over 21
    if score > 21:
        # replace aces (value 11) with value 1 until there
        # are no more aces or the score is 21 or less
        while score > 21 and ace in hand:
            # ace_index = hand.index(ace)
            # hand[ace_index] = 1
            hand.remove(ace)
            hand.append(1)
            score -= 10

    # don't need to return hand -
    return score

def display_hand(hand, is_player, is_final):
    """
    displays hand and score
    :param hand: player's/dealer's hand
    :param is_player: True if the player's hand, False if the dealer's hand
    :param is_final: if True is the final hand, if False is the current hand
    :return: string containing player name, hand and score
    """
    message = ""
    if is_final:
        message += "   "
    else:
        message += "\t"

    # player name
    if is_player:
        message += "Your "
    else:
        message += "Computer's "

    # hand text
    if is_final:
        message += "final hand "
    else:
        # if the number of cards is more than one, display the plural
        # if the dealer and the number of cards is 2, only show the first card
        if is_player or (not is_player and len(hand) > 2):
            message += "cards: "
        else:
            # only shown before the dealer gets a turn
            message += "first card: "

    # cards
    if is_player or (not is_player and len(hand) > 2 or is_final):
        # show all cards if the cards are from the player or
        #   the cards are from the dealer and there are more than 2 cards or
        #   the cards are from the dealer and everyone has played
        message += f"[{(", ".join(str(card) for card in hand))}]"
    else:
        message += str(hand[0])

    # total score
    if is_player or (not is_player and len(hand) > 2):
        # only show score if the cards are the player's cards or
        # the cards are the dealer's and there are more than 2 cards

        total_hand = calculate_score(hand=hand)
        score_decorator = "current"
        if is_final:
            score_decorator = "final"
        message += f", {score_decorator} score: {total_hand}"

    return message

def determine_winner(player_score, dealer_score, is_first_round, player_passed):
    """
    determine if the player won, the dealer won, or if it is a draw
    :param player_score: sum of the player's cards
    :param dealer_score: sum of the dealer's cards
    :param is_first_round: True if the player hasn't drawn any cards
    :param player_passed: True if the player has passed on drawing another card,
        False if the player is still drawing cards
    :return: "Player", "Dealer", or "Draw"
    """
    # Check if either the player or the dealer went over 21
    # If the player or dealer went over 21 they immediately lose, regardless of the
    # score of the opponent.
    if player_score > 21:
        return "You went over. You lose! 😥"
    elif dealer_score > 21:
        return "Opponent went over. You win! 😎"

    # check if either the player or the dealer had blackjack on the initial
    # dealing of cards
    if is_first_round:
        if player_score == 21 and dealer_score == 21:
            return "Dealer wins with Blackjack! 🤣"
        elif player_score == 21:
            return "You win with Blackjack! 😂"
        elif dealer_score == 21:
            return "Dealer wins with Blackjack! 😒"
    elif player_passed:
        # no blackjack, and the player/dealer's score is 21 or less
        if player_score == dealer_score:
            return "The game is a draw. 😐"
        elif player_score > dealer_score:
            return "Player wins! 🎆"
        else:
            return "Dealer wins! 😶‍🌫️"
    else:
        # player is still playing.
        # until the player opts to not draw another card there is no winner
        return None

def deal_card():
    """
    randomly picks a card from the deck
    :return: int indicating the value of the card
    """
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

def play_player(player_hand, dealer_hand):
    """
    handles the player part of the game
    :param player_hand: player's hand of cards
    :param dealer_hand: dealer's hand of cards
    :return: boolean indicating that the player busted, player's hand of cards
    """
    show_hands(player_hand=player_hand, dealer_hand=dealer_hand, is_final=False)

    # 1 - ask if the player wants another card
    continue_playing = True
    # 2 - while the player wants another card:
    while continue_playing:
        get_card = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        if get_card == 'y':
            #   a - deal 1 card to the player using deal_card()
            player_hand.append(deal_card())
            #   b - calculate player hand and score using calculate_score()
            player_score = calculate_score(player_hand)
            #   c - display player and dealer's hands
            show_hands(player_hand=player_hand, dealer_hand=dealer_hand, is_final=False)

            if player_score >= 21:
                return (player_score > 21), player_hand
        else:
            continue_playing = False

    return False, player_hand

def play_dealer(dealer_hand):
    """
    handles the dealer's turn in the game
    :param dealer_hand: dealer's hand of cards
    :return: dealer's hand once the score is over 16
    """
    dealer_score = calculate_score(dealer_hand)
    while dealer_score < 17:
        dealer_hand.append(deal_card())
        dealer_score = calculate_score(dealer_hand)

    return dealer_hand

def show_hands(player_hand, dealer_hand, is_final):
    """
    display the player and dealer hand and scores
    :param player_hand: player's hand of cards
    :param dealer_hand: dealer's hand of cards
    :param is_final: True if this will be the final display of hands and scores, False if not
    """
    print(display_hand(hand=player_hand, is_player=True, is_final=is_final))
    print(display_hand(hand=dealer_hand, is_player=False, is_final=is_final))

def play_game():
    clear_screen()
    print(art.logo)

    # initialize the player and dealer hands, then deal two cards
    # to each hand
    p_hand = []
    d_hand = []
    for _ in range(2):
        p_hand.append(deal_card())
        d_hand.append(deal_card())

    # calculate scores, update hands (shouldn't replace any cards at this point)
    p_score = calculate_score(p_hand)
    d_score = calculate_score(d_hand)

    first_round = determine_winner(
        player_score=p_score, dealer_score=d_score, is_first_round=True, player_passed=False)

    if first_round is not None:
        # either the player, dealer, or both had Blackjack
        show_hands(player_hand=p_hand, dealer_hand=d_hand, is_final=True)
        print(first_round)
    else:
        # run through the player's part of the game.
        # if True is returned the player went over 21
        player_busted, p_hand = play_player(player_hand=p_hand, dealer_hand=d_hand)

        # the dealer will not play if the player busted
        if not player_busted:
            # run through dealer's part of the game
            d_hand = play_dealer(dealer_hand=d_hand)

        # final calculation of scores and hand
        p_score = calculate_score(p_hand)
        d_score = calculate_score(d_hand)

        show_hands(player_hand=p_hand, dealer_hand=d_hand, is_final=True)

        print(determine_winner(
            player_score=p_score, dealer_score=d_score, is_first_round=False,
            player_passed=True))

# # test calculate_score
# # test_hand = [4, 5, 11, 10]
# # print(test_hand)
# # result = calculate_score(hand=test_hand)
# # print(result)
# # print(test_hand)

# play the game!
play_a_game = True
while play_a_game:
    play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
    if play != 'y':
        play_a_game = False
    else:
        play_game()
        # clear_screen()
        # print(art.logo)
        #
        # # initialize the player and dealer hands, then deal two cards
        # # to each hand
        # p_hand = []
        # d_hand = []
        # for _ in range(2):
        #     p_hand.append(deal_card())
        #     d_hand.append(deal_card())
        #
        # # calculate scores, update hands (shouldn't replace any cards at this point)
        # p_score = calculate_score(p_hand)
        # d_score = calculate_score(d_hand)
        #
        # first_round = determine_winner(
        #     player_score=p_score, dealer_score=d_score, is_first_round=True, player_passed=False)
        #
        # if first_round is not None:
        #     # either the player, dealer, or both had Blackjack
        #     show_hands(player_hand=p_hand, dealer_hand=d_hand, is_final=True)
        #     print(first_round)
        # else:
        #     # run through the player's part of the game.
        #     # if True is returned the player went over 21
        #     player_busted, p_hand = play_player(player_hand=p_hand, dealer_hand=d_hand)
        #
        #     # the dealer will not play if the player busted
        #     if not player_busted:
        #         # run through dealer's part of the game
        #         d_hand = play_dealer(dealer_hand=d_hand)
        #
        #     # final calculation of scores and hand
        #     p_score = calculate_score(p_hand)
        #     d_score = calculate_score(d_hand)
        #
        #     show_hands(player_hand=p_hand, dealer_hand=d_hand, is_final=True)
        #
        #     print(determine_winner(
        #         player_score=p_score, dealer_score=d_score, is_first_round=False,
        #         player_passed=True))

