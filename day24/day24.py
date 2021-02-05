from collections import defaultdict
import pprint

direction_to_idx = {"e": 0, "se": 1, "sw": 2, "w": 3, "nw": 4, "ne": 5}


def parse_directions(input_filename):
    directions = []

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")

            parsed_line = []
            i = 0
            while i < len(line):
                char = line[i]

                if char in {"n", "s"}:
                    i = i + 1
                    next_char = line[i]
                    parsed_line.append(char + next_char)
                else:  # e or w
                    assert char in {"e", "w"}, "something bad happened"
                    parsed_line.append(char)
                i = i + 1
            directions.append(parsed_line)

    return directions


def canonicalize_directions(directions):
    relative_distance = [0] * 6

    # count the relative steps in each direction
    for direction in directions:
        direction_idx = direction_to_idx[direction]
        relative_distance[direction_idx] += 1

    return canonicalize_relative_distance(relative_distance)


def canonicalize_relative_distance(relative_distance):
    canonicalize = {
        # pairs of directions that reduce to one
        ("e", "nw"): "ne",
        ("ne", "w"): "nw",
        ("nw", "sw"): "w",
        ("w", "se"): "sw",
        ("sw", "e"): "se",
        ("se", "ne"): "e",
        # opposing directions cancel each other out
        ("e", "w"): None,
        ("se", "nw"): None,
        ("sw", "ne"): None,
    }

    more_to_canonicalize = True

    while more_to_canonicalize:
        more_to_canonicalize = False

        for pairs, reduction in canonicalize.items():
            pair1_idx = direction_to_idx[pairs[0]]
            pair2_idx = direction_to_idx[pairs[1]]
            reduction_idx = direction_to_idx[reduction] if reduction else None

            pair1_count = relative_distance[pair1_idx]
            pair2_count = relative_distance[pair2_idx]

            if pair1_count > 0 and pair2_count > 0:
                more_to_canonicalize = True

                if reduction_idx is None:  # opposing directions
                    num_to_cancel = min(pair1_count, pair2_count)
                    relative_distance[pair1_idx] = pair1_count - num_to_cancel
                    relative_distance[pair2_idx] = pair2_count - num_to_cancel
                else:  # reductions
                    num_to_reduce = min(pair1_count, pair2_count)
                    relative_distance[reduction_idx] += num_to_reduce
                    relative_distance[pair1_idx] = pair1_count - num_to_reduce
                    relative_distance[pair2_idx] = pair2_count - num_to_reduce

    return tuple(relative_distance)


def is_neighbor(direction, other_direction):
    # should be a total of 1 away in any direction
    distances = []

    # relative distance at each position
    for position in range(len(direction)):
        distances.append(abs(direction[position] - other_direction[position]))

    # and canonicalize
    distances = canonicalize_relative_distance(distances)

    # and compute distance
    total_distance = sum(distances)

    return total_distance == 1


def count_black_neighbors(direction, tile_flips):
    black_count = 0

    for i in range(len(direction)):
        neighbor = list(direction)
        neighbor[i] += 1
        neighbor = canonicalize_relative_distance(neighbor)

        if neighbor in tile_flips and is_black(tile_flips[neighbor]):
            black_count += 1

    return black_count


def is_black(flip_count):
    return flip_count % 2 == 1  # flipped an odd number of times


def enumerate_all_black_neighbor_tiles(tile_flips):
    all_tiles = set()

    for canonical_direction, flip_count in tile_flips.items():
        if is_black(flip_count):  # only care about neighbors of black tiles
            for i in range(len(canonical_direction)):  # enumerate 1 position differences for all directions
                neighbor = list(canonical_direction)
                neighbor[i] += 1

                all_tiles.add(canonicalize_relative_distance(neighbor))
            all_tiles.add(canonical_direction)  # already canonicalized

    return all_tiles


def next_day(tile_flips):
    next_tile_flips = tile_flips.copy()

    for canonical_direction, flip_count in tile_flips.items():
        black_count = count_black_neighbors(canonical_direction, tile_flips)

        # black tile + 0 or > 2 black tiles --> flipped to white
        # white + 2 black --> black
        if is_black(flip_count):
            if black_count == 0 or black_count > 2:
                next_tile_flips[canonical_direction] += 1  # flip to white
        else:  # white
            if black_count == 2:
                next_tile_flips[canonical_direction] += 1  # flip to black

    return next_tile_flips


def count_black(tile_flips):
    num_flips = 0
    for _, flip_count in tile_flips.items():
        if is_black(flip_count):
            num_flips += 1

    return num_flips


def expand_tiles(tile_flips):
    all_relevant_tiles = enumerate_all_black_neighbor_tiles(tile_flips)

    for canonical_direction in all_relevant_tiles:
        if canonical_direction not in tile_flips:
            tile_flips[canonical_direction] = 0


if __name__ == "__main__":
    # need a way to index tiles and how many times they've been flipped
    # directions are: ne, nw, e, w, se, sw
    tile_flips = defaultdict(int)  # keyed by (e, se, sw, w, nw, ne) --> # of flips
    directions = parse_directions("day24_input.txt")

    for line, direction in enumerate(directions):
        canonical_direction = canonicalize_directions(direction)
        tile_flips[canonical_direction] += 1

    # include other tiles not directly referenced in input file
    expand_tiles(tile_flips)

    for i in range(100):
        tile_flips = next_day(tile_flips)
        print(f"Day {i+1}: {count_black(tile_flips)}")
        expand_tiles(tile_flips)

    # print(canonicalize_directions(["e", "se", "w"]))
    # print(canonicalize_directions(["nw", "w", "sw", "e", "e"]))
