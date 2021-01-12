def get_number(starting_numbers, turn):
    num_starting_numbers = len(starting_numbers)
    last_seen_idx = dict()
    for i, num in enumerate(starting_numbers[: len(starting_numbers) - 1]):
        last_seen_idx[num] = i
    last_spoken = starting_numbers[-1]

    for i in range(turn - len(starting_numbers)):
        actual_turn_no = i + num_starting_numbers + 1
        idx = find_last_mention(last_seen_idx, last_spoken)
        # print("at turn", actual_turn_no)
        # print("looking for", last_spoken)
        # print("found at idx", idx)

        if idx is None:
            next_ = 0
        else:
            last_turn_spoken = idx + 1
            # print("last spoken at turn", last_turn_spoken)
            next_ = (actual_turn_no - 1) - last_turn_spoken

        # print("number at this turn will be", next_)
        # print("-----")
        last_seen_idx[last_spoken] = actual_turn_no - 2
        last_spoken = next_

    return last_spoken


def find_last_mention(last_seen_idx, number):
    # idx = None
    #
    # for i in range(len(numbers)-1, -1, -1):
    #     if numbers[i] == number:
    #         idx = i
    #         break
    #
    # return idx
    return last_seen_idx.get(number, None)


if __name__ == "__main__":
    # print(get_number([0,3,6], 10))
    print(get_number([2, 0, 6, 12, 1, 3], 30000000))
