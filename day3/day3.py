def find_solution(input_filename):
    grid = []

    for row in open(input_filename, "r"):
        grid.append([True if cell == "#" else False for cell in row.rstrip("\n")])

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]  # right 3, down 1

    num_trees = [traverse_slopes(grid, slope) for slope in slopes]

    product = 1
    for t in num_trees:
        product = product * t
    return product


def traverse_slopes(grid, slope):
    row = 0
    position_in_row = 0
    num_trees = 0
    num_not_trees = 0

    while row < len(grid):  # haven't gotten to the bottom yet
        # take into account right wrapping
        if position_in_row >= len(grid[row]):
            position_in_row = position_in_row % len(grid[row])
        # print("position is", row, position_in_row)
        # print(grid[row])
        # print(grid[row][position_in_row])

        # is_tree ?
        if grid[row][position_in_row]:
            num_trees = num_trees + 1
        else:
            num_not_trees = num_not_trees + 1

        # take next step
        position_in_row = position_in_row + slope[0]
        row = row + slope[1]

    # print(num_trees, num_not_trees)  yes, counting all the rows
    return num_trees


if __name__ == "__main__":
    num_trees = find_solution("day3_input.txt")
    print(num_trees)
