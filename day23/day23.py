def pick3_cards(cups, index):
    print(cups)

    # pick up three cups immediately clockwise of current and remove
    #  if lower than any cup then wraps around to highest cup label instead
    start = index + 1
    end = index + 4

    if start > len(cups):  # on last item
        start = start % len(cups)  # should always be zero
        end = end % len(cups)
        pick3 = cups[start:end]
        cups = cups[end:]
    elif end > len(cups):  # need some from end, and some from beginning
        pick3 = cups[start:]
        remainder = 3 - len(pick3)
        pick3 += cups[:remainder]

        cups = cups[remainder:start]
    else:  # all in the middle
        pick3 = cups[start:end]

        cups = cups[:start] + cups[end:]

    print("pick3", pick3)
    return pick3, cups


def get_destination_index(cups, current_cup):
    # destination cup = cup w/current label - 1, if above keep subtracting 1 until not.
    target = current_cup - 1
    target_index = -1

    while target not in cups:
        if target < min(cups):
            target = max(cups)
            target_index = cups.index(target)
            break

        target = target - 1

    if target_index == -1:
        target_index = cups.index(target)

    return target_index


def shift_to_target(cups, current_cup, destination_index):
    next_cups = cups.copy()

    while next_cups[destination_index] != current_cup:
        last_item = len(next_cups) - 1  # rotate last item to the front
        next_cups = [next_cups[last_item]] + next_cups[:last_item]

    return next_cups


def get_clockwise_order_after1(cups):
    one_index = cups.index(1)

    rotated = cups[one_index:] + cups[:one_index]
    return rotated[1:]


if __name__ == "__main__":
    # cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    cups = [3, 9, 8, 2, 5, 4, 7, 1, 6]

    for i in range(100):
        index = i % len(cups)
        print("*****")
        print("move", i + 1)
        current_cup = cups[index]
        print("current cup", current_cup)
        pick3, cups = pick3_cards(cups, index)
        destination_idx = get_destination_index(cups, current_cup)
        print("destination", cups[destination_idx])
        # cups picked up immediately clockwise of destination cup
        cups = cups[: destination_idx + 1] + pick3 + cups[destination_idx + 1 :]
        # shift until current_cup is back in position index
        cups = shift_to_target(cups, current_cup, index)
    print("finally", "".join(map(str, get_clockwise_order_after1(cups))))
