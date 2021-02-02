def pick3_ll(right_pointers, current_cup):
    pick3 = []
    next_ = right_pointers[current_cup]

    for _ in range(3):
        pick3.append(next_)
        next_ = right_pointers[next_]

    # chop out the picked list
    right_pointers[current_cup] = next_

    for label in pick3:
        del right_pointers[label]

    return pick3, right_pointers


def get_destination_ll(right_pointers, current_cup, min_, max_):
    # need an efficient way to find min and max here
    target = current_cup - 1

    while target not in right_pointers:
        if target < min_:
            target = max_
            break

        target = target - 1

    return target


def get_clockwise_order_after1_ll(right_pointers):
    labels = []
    ptr = right_pointers[1]

    while ptr != 1:
        labels.append(ptr)
        ptr = right_pointers[ptr]

    return labels


def initialize_right_pointers(cups):
    right_pointers = {}
    prev_cup = None

    for cup in cups:
        if not prev_cup:  # first element
            prev_cup = cup
        else:
            right_pointers[prev_cup] = cup
            prev_cup = cup

    right_pointers[prev_cup] = cups[0]  # complete the circle

    return right_pointers


def find_min_max(sorted_cups, pick3):
    idx_min = 0
    idx_max = len(sorted_cups) - 1
    min_, max_ = sorted_cups[idx_min], sorted_cups[idx_max]

    while min_ in pick3:
        idx_min = idx_min + 1
        min_ = sorted_cups[idx_min]

    while max_ in pick3:
        idx_max = idx_max - 1
        max_ = sorted_cups[idx_max]

    return min_, max_


if __name__ == "__main__":
    # cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    cups = [3, 9, 8, 2, 5, 4, 7, 1, 6]
    fill_size = 1000000
    biggest = max(cups)
    cups += list(map(lambda x: biggest + x, range(1, fill_size - len(cups) + 1)))  # fill up to 1M
    sorted_cups = sorted(cups)

    right_pointers = initialize_right_pointers(cups)

    # part 2:
    # - one million cups! remaining cups are max+1, max+2, ... max+n
    # - 10 million moves!
    # - find two cups immediately clockwise of cup 1

    i = 0
    current_cup = cups[0]

    while i < 10000000:
        # print("*** move", i+1)
        # print(right_pointers)
        pick3, right_pointers = pick3_ll(right_pointers, current_cup)
        # print("pick3", pick3)

        min_, max_ = find_min_max(sorted_cups, pick3)

        # find destination and insert, no need to shift
        destination = get_destination_ll(right_pointers, current_cup, min_, max_)
        # print("destination", destination)
        old_dest_right_ptr = right_pointers[destination]

        for label in pick3:
            right_pointers[destination] = label
            destination = label

        right_pointers[pick3[2]] = old_dest_right_ptr

        current_cup = right_pointers[current_cup]
        i = i + 1

    # print("finally", "".join(map(str, get_clockwise_order_after1_ll(right_pointers))))

    after_one = right_pointers[1]
    after_after_one = right_pointers[after_one]
    print(after_one * after_after_one)
