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


def play_hands(player1_hand, player2_hand):

    while player1_hand and player2_hand:
        # print("player 1 hand:", player1_hand)
        # print("player 2 hand:", player2_hand)
        player1_card = player1_hand.pop(0)
        player2_card = player2_hand.pop(0)

        if player1_card > player2_card:
            player1_hand.extend([player1_card, player2_card])
        else:
            player2_hand.extend([player2_card, player1_card])

    return player1_hand, player2_hand


def calculate_score(winning_hand):
    score = 0

    multiplier = 1
    for i in range(len(winning_hand) - 1, -1, -1):
        card = winning_hand[i]
        score += card * multiplier
        multiplier += 1

    return score


if __name__ == "__main__":
    player1_hand, player2_hand = load_hands("day22_input.txt")
    player1_hand, player2_hand = play_hands(player1_hand, player2_hand)
    winning_hand = player1_hand if player1_hand else player2_hand
    # print(winning_hand)
    print(calculate_score(winning_hand))
