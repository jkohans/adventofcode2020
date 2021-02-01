def load_hands(input_filename):
    is_player1 = True
    player1_hand = []
    player2_hand = []

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")
            if line in ("Player 1:", ""):
                continue

            if line == "Player 2:":
                is_player1 = False
                continue

            if is_player1:
                player1_hand.append(int(line))
            else:
                player2_hand.append(int(line))

    return player1_hand, player2_hand


def check_recursive_combat(player1_card, player2_card, player1_hand, player2_hand):
    return len(player1_hand) >= player1_card and len(player2_hand) >= player2_card


def play_recursive_combat(player1_hand, player2_hand):
    prev_player1_hands = set()
    prev_player2_hands = set()
    is_player1_winner = False

    while player1_hand and player2_hand:
        print("**********")
        print("player 1 hand:", player1_hand)
        print("player 2 hand:", player2_hand)

        # 1. before deal: prev rd with same cards in same order in same player's hand --> player 1 wins
        if tuple(player1_hand) in prev_player1_hands or tuple(player2_hand) in prev_player2_hands:
            print("I'm so done")
            is_player1_winner = True
            break

        prev_player1_hands.add(tuple(player1_hand))
        prev_player2_hands.add(tuple(player2_hand))

        player1_card = player1_hand.pop(0)
        player2_card = player2_hand.pop(0)
        print("player 1 card:", player1_card)
        print("player 2 card:", player2_card)

        # 2. after deal: both w/at least as many cards in deck as value of card just drew --> recursive combat!
        #  2a. otherwise, winner is higher value card
        if check_recursive_combat(player1_card, player2_card, player1_hand, player2_hand):
            # slices make a copy, so should be ok here
            _, is_player1_winner = play_recursive_combat(player1_hand[:player1_card], player2_hand[:player2_card])
        else:
            is_player1_winner = player1_card > player2_card

        if is_player1_winner:
            player1_hand.extend([player1_card, player2_card])
        else:
            player2_hand.extend([player2_card, player1_card])

    if is_player1_winner:
        print("player 1 winner!")
        return player1_hand, True
    else:
        print("player 2 winner!")
        return (player1_hand, True) if player1_hand else (player2_hand, False)


def calculate_score(winning_hand):
    score = 0

    for multiplier, card in enumerate(reversed(winning_hand), start=1):
        score += card * multiplier

    return score


if __name__ == "__main__":
    player1_hand, player2_hand = load_hands("day22_input.txt")
    winning_hand, _ = play_recursive_combat(player1_hand, player2_hand)
    print(winning_hand)
    print(calculate_score(winning_hand))
