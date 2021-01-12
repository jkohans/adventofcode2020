def solve_problem(input_filename):
    num_valid = 0
    num_invalid = 0

    for line in open(input_filename, "r"):
        range, letter, password = line.split()
        letter = letter[0]  # discard colon
        min, max = (int(x) for x in range.split("-"))
        letter_count = sum(1 for l in password if l == letter)
        # print(min, max, letter, password)

        if min <= letter_count <= max:
            num_valid = num_valid + 1
        else:
            num_invalid = num_invalid + 1

    return num_valid


def part_two(input_filename):
    num_valid = 0
    num_invalid = 0

    for line in open(input_filename, "r"):
        range, letter, password = line.split()
        letter = letter[0]  # discard colon
        idx1, idx2 = (int(x) for x in range.split("-"))

        # no index out of bounds checking needed here?
        is_valid = (letter == password[idx1 - 1]) ^ (letter == password[idx2 - 1])
        if is_valid:
            num_valid = num_valid + 1
        else:
            num_invalid = num_invalid + 1

    return num_valid


if __name__ == "__main__":
    # num_valid = solve_problem("day2_input.txt")
    # print(num_valid)

    num_valid = part_two("day2_input.txt")
    print(num_valid)
