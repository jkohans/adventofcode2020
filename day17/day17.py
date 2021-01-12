import copy
import pprint


def read_init_configuration(input_filename):
    cubes = []

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip()
            cubes.append([cube for cube in line])

    return [[cubes]]  # cubes within z and w dims


def get_neighbor_count(hypercube, w, z, x, y):
    print("getting neighbor count for", w, z, x, y)
    neighbor_count = 0

    for hyper in range(w - 1, w + 2):
        for dim in range(z - 1, z + 2):
            for row in range(x - 1, x + 2):
                for col in range(y - 1, y + 2):
                    if (hyper, dim, row, col) == (w, z, x, y):  # don't count self
                        continue

                    if not 0 <= hyper < len(hypercube):
                        continue

                    if not 0 <= dim < len(hypercube[w]):  # reached a dim that doesn't exist
                        continue

                    if not 0 <= row < len(hypercube[w][dim]):  # out of bounds on row
                        continue

                    if not 0 <= col < len(hypercube[w][dim][row]):  # out of bounds on col
                        continue

                    if hypercube[w][dim][row][col] == "#":
                        neighbor_count += 1

    return neighbor_count


# def gen_inactive_slice(cube_slices):
#     slice = []
#     cube = cube_slices[0]
#
#     x = len(cube)
#     y = len(cube[0])
#
#     for _ in range(x):
#         slice.append(["." for _ in range(y)])
#
#     return slice


def pad_by_shape(shape):
    if not isinstance(shape, list):
        return "."

    return [pad_by_shape(item) for item in shape]


def pad_hypercube(hypercube):
    padded = pad_by_shape(hypercube) + hypercube + pad_by_shape(hypercube)

    for w in range(len(padded)):
        padded[w] = pad_by_shape(padded[w]) + padded[w] + pad_by_shape(padded[w])

        for z in range(len(padded[w])):
            next_dim = padded[w][z]
            padded[w][z] = pad_by_shape(next_dim) + next_dim + pad_by_shape(next_dim)

            for x in range(len(padded[w][z])):
                next_dim = padded[w][z][x]

                padded[w][z][x] = pad_by_shape(next_dim) + next_dim + pad_by_shape(next_dim)

                # what about y here??

    return padded

    # # padding functions
    # hypercube = [gen_inactive_slice(hypercube)] + hypercube + [gen_inactive_slice(hypercube)]
    #
    # # for each cube in the slice, pad the top, bottom, left and right
    # for slice_idx in range(len(hypercube)):
    #     cube = hypercube[slice_idx]
    #     row_size = len(cube)
    #
    #     cube = [["." for _ in range(row_size)]] + cube + [["." for _ in range(row_size)]]  # top + bottom
    #     for col in range(len(cube)):
    #         cube[col] = ["."] + cube[col] + ["."]  # left and right
    #     hypercube[slice_idx] = cube
    #
    # return hypercube


def get_next_state(hypercube):
    hypercube = pad_hypercube(hypercube)
    next_cubes = copy.deepcopy(hypercube)

    for w in range(len(hypercube)):
        for z in range(len(hypercube[w])):
            cube = hypercube[w][z]
            for x in range(len(cube)):
                row = cube[x]
                for y in range(len(row)):
                    num_active = get_neighbor_count(hypercube, w, z, x, y)

                    # active + 2-3 --> remains active, otherwise inactive
                    # inactive + exactly 3 active --> active, otherwise inactive
                    if hypercube[w][z][x][y] == "#":  # active cell
                        if num_active not in {2, 3}:
                            next_cubes[w][z][x][y] = "."
                    else:  # inactive cell
                        if num_active == 3:
                            next_cubes[w][z][x][y] = "#"

    return next_cubes


def count_active(hypercube):
    num_active = 0

    for w in range(len(hypercube)):
        for z in range(len(hypercube[w])):
            for x in range(len(hypercube[w][z])):
                for y in range(len(hypercube[w][z][x])):
                    if hypercube[w][z][x][y] == "#":
                        num_active += 1

    return num_active


# NEW approach below


def read_init_configuration_into_set(input_filename):
    active_cubes = set()
    y_size = 0

    with open(input_filename) as f:
        x_size = 0
        for x, line in enumerate(f):
            x_size += 1
            line = line.rstrip()
            y_size = 0
            for y, cube in enumerate(line):
                y_size += 1
                if cube == "#":
                    active_cubes.add((0, 0, x, y))

    return active_cubes, [1, 1, x_size, y_size]


def count_active_from_set(cubes):
    return len(cubes)


def check_bounds(coords, dim):
    for i in range(len(coords)):
        if not 0 <= coords[i] < dim[i]:
            return False

    return True


def get_next_state_from_set(active_cubes, dims):
    next_active_cubes = set()
    visited = set()

    for (w, z, x, y) in active_cubes:  # look around the active cubes, including the active cube itself
        for dw in range(w - 1, w + 2):
            for dz in range(z - 1, z + 2):
                for dx in range(x - 1, x + 2):
                    for dy in range(y - 1, y + 2):
                        coords = (dw, dz, dx, dy)

                        if coords in visited:
                            continue
                        else:
                            visited.add(coords)

                        if not check_bounds(coords, dims):  # is off the hypercube
                            continue

                        num_active = get_neighbor_count_from_set(active_cubes, coords)

                        # active + 2-3 --> remains active, otherwise inactive
                        # inactive + exactly 3 active --> active, otherwise inactive
                        if coords in active_cubes:  # active cell
                            if num_active in {2, 3}:
                                next_active_cubes.add(coords)
                        else:  # inactive cell
                            if num_active == 3:
                                next_active_cubes.add(coords)

    return next_active_cubes


def shift_coords(active_cubes):
    return {(w + 1, z + 1, x + 1, y + 1) for (w, z, x, y) in active_cubes}


def is_neighbor(cube, coords):
    if cube == coords:
        return False

    for i in range(len(cube)):
        dist = cube[i] - coords[i]
        if abs(dist) > 1:  # the distance between 2 points in the same dim are > 1
            return False

    return True


def get_neighbor_count_from_set(active_cubes, coords):
    num_active_neighbors = 0

    for cube in active_cubes:
        if is_neighbor(cube, coords):
            num_active_neighbors += 1

    return num_active_neighbors


if __name__ == "__main__":
    active_cubes, dims = read_init_configuration_into_set("input_day17.txt")
    next_ = None

    for i in range(6):
        print("After cycle", i + 1)
        dims = [dim + 2 for dim in dims]  # at each generation you expand the dims by 1 on each side
        active_cubes = shift_coords(active_cubes)  # you also need to shift the current active cubes accordingly
        next_ = get_next_state_from_set(active_cubes, dims)
        active_cubes = next_
        print(count_active_from_set(next_))
