import copy
import numpy as np


def get_occupied_seats(input_filename):
    matrix = []

    # L - empty
    # # - occupied
    # . - floor
    with open(input_filename) as f:
        for line in f:
            matrix.append([c for c in line.rstrip("\n")])

    next_matrix = get_next_gen(matrix)

    while matrix != next_matrix:
        matrix, next_matrix = next_matrix, get_next_gen(next_matrix)
        # print(np.matrix(matrix))

    return count_occupied(matrix)


def count_occupied(matrix):
    count = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "#":
                count = count + 1

    return count


def count_occupied_visible_seats(matrix, i, j):
    # follow all 8 directions, until something other than floor is seen
    deltas = []
    count = 0

    for row in [-1, 0, 1]:
        for column in [-1, 0, 1]:
            delta = (row, column)
            if not (row, column) == (0, 0):
                deltas.append(delta)

    for delta in deltas:
        seat = get_next_visible_seat(matrix, i, j, delta)
        if seat == "#":
            count = count + 1

    return count


def get_next_visible_seat(matrix, i, j, delta):
    position = (i + delta[0], j + delta[1])

    while 0 <= position[0] < len(matrix) and 0 <= position[1] < len(matrix[position[0]]):
        seat = matrix[position[0]][position[1]]
        if seat != ".":
            return seat
        next_position = (position[0] + delta[0], position[1] + delta[1])
        position = next_position

    return None


def count_occupied_adjacent_neigbors(matrix, i, j):
    occupied_count = 0

    for row in [i - 1, i, i + 1]:
        for column in [j - 1, j, j + 1]:
            if not (row, column) == (i, j) and 0 <= row < len(matrix) and 0 <= column < len(matrix[row]):
                if matrix[row][column] == "#":
                    occupied_count = occupied_count + 1

    return occupied_count


def get_next_gen(matrix):
    next_matrix = copy.deepcopy(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # occupied_count = count_occupied_adjacent_neigbors(matrix, i, j)
            occupied_count = count_occupied_visible_seats(matrix, i, j)

            # rules:
            # L and no adjacent --> occupied
            # # and 4 or more adjacent --> empty
            # otherwise, no change
            if matrix[i][j] == "L" and occupied_count == 0:
                next_matrix[i][j] = "#"
            elif matrix[i][j] == "#" and occupied_count >= 5:  # and occupied_count >= 4:
                next_matrix[i][j] = "L"

    return next_matrix


if __name__ == "__main__":
    num_occupied = get_occupied_seats("input_day11.txt")
    print(num_occupied)
