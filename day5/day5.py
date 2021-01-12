import math


def find_passport(input_filename):
    num_rows = 128
    num_columns = 8
    seat_codes = []
    current_max = 0

    for line in open(input_filename):
        line = line.rstrip("\n")
        row_directions = line[:7]
        column_directions = line[7:]

        row_answer = bin_search(num_rows, row_directions, "F", "B")
        column_answer = bin_search(num_columns, column_directions, "L", "R")
        # print(row_answer, column_answer)
        # print("------------")
        seat_code = row_answer * 8 + column_answer
        seat_codes.append(seat_code)

        if seat_code > current_max:
            current_max = seat_code

    return seat_codes


def find_missing_seat(seat_codes):
    seat_codes.sort()

    for idx, id in enumerate(seat_codes):
        if idx - 1 >= 0:  # check that lower number is right
            if seat_codes[idx - 1] != id - 1:
                return id - 1


def bin_search(num_items, directions, lower_string, upper_string):
    current_range = (0, num_items)  # max is exclusive

    for direction in directions:
        # print(direction)
        if direction == upper_string:
            new_min = current_range[0] + math.ceil((current_range[1] - current_range[0]) / 2)
            current_range = (new_min, current_range[1])
        elif direction == lower_string:
            new_max = current_range[1] - math.floor((current_range[1] - current_range[0]) / 2)
            current_range = (current_range[0], new_max)
        else:
            print("shit done broke on unknown direction", direction)
            exit(1)
        # print(current_range)

    if not (0 <= current_range[0] < num_items):
        print("chose an index out of range", current_range[0], num_items)
        exit(1)

    return current_range[0]


if __name__ == "__main__":
    seat_codes = find_passport("day5_input.txt")
    print(find_missing_seat(seat_codes))
