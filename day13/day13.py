from functools import reduce


def get_earliest_bus(timestamp, buses):
    earliest_arrival = None

    for bus in buses:
        next_arrival = bus
        while next_arrival <= timestamp:
            next_arrival = next_arrival + bus

        time_to_wait = next_arrival - timestamp

        if not earliest_arrival:
            earliest_arrival = (bus, time_to_wait)
        elif time_to_wait < earliest_arrival[1]:
            earliest_arrival = (bus, time_to_wait)

    return earliest_arrival


def get_sequence(x, y, difference):
    xs = {i * x for i in range(1, x * y)}
    ys = [i * y for i in range(1, x * y)]

    for iy, y in enumerate(ys):
        # looking for x + difference = y
        if y - difference in xs:
            # yield (int((y - difference)/x), iy+1)
            yield (y - difference, y)


def generate_stream(sequence_generator):
    first = next(sequence_generator)
    second = next(sequence_generator)
    yield first
    delta = (second[0] - first[0], second[1] - first[1])
    current = first

    while True:
        next_ = (current[0] + delta[0], current[1] + delta[1])
        yield next_
        current = next_


def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


if __name__ == "__main__":
    input_filename = "day13_input.txt"

    with open(input_filename) as f:
        timestamp = int(f.readline().rstrip("\n"))
        # buses = [int(id) for id in f.readline().rstrip("\n").split(",") if id != 'x']
        buses = f.readline().rstrip("\n").split(",")

    # part1
    # bus, time_to_wait = get_earliest_bus(timestamp, buses)
    # print(bus * time_to_wait)

    # part2
    # buses = ["17", "x", "13", "19"]

    # stream1 = generate_stream(get_product_offsets(17, 13, 2))
    # print([next(stream1) for i in range(10)])
    #
    # # print(list(get_product_offsets(13, 19, 1)))

    # prev_idx = 0
    # next_idx = 1
    # offsets = []

    n = []
    a = []

    for i, bus_id in enumerate(buses):
        if bus_id != "x":
            bus_id = int(bus_id)
            n.append(bus_id)
            a.append(bus_id - i)
    print(chinese_remainder(n, a))

    # for first in generate_stream(get_sequence(17, 13, 2)):
    #     print("first", first)
    #     for second in generate_stream(get_sequence(13, 19, 1)):
    #         print("second", second)
    #         if second[0] > first[1]:
    #             break
    #
    #         if first[1] == second[0]:
    #             print("found!", first, second)
    #             exit(1)

    # while next_idx < len(buses):
    #     # scan past x's
    #     difference = 1
    #     while buses[next_idx] == "x":
    #         difference = difference + 1
    #         next_idx = next_idx + 1
    #
    #     stream = generate_stream(get_sequence(int(buses[prev_idx]), int(buses[next_idx]), difference))
    #     offsets.append(stream)
    #     prev_idx, next_idx = next_idx, next_idx + 1
    #
    # for stream in offsets:
    #     print([next(stream) for _ in range(20)])
