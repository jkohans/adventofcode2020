from collections import defaultdict
import pprint


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
    final_location = [0] * 6
    direction_to_idx = {"e": 0, "se": 1, "sw": 2, "w": 3, "nw": 4, "ne": 5}

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

    # count the relative steps in each direction
    for direction in directions:
        direction_idx = direction_to_idx[direction]
        final_location[direction_idx] += 1

    more_to_canonicalize = True

    while more_to_canonicalize:
        more_to_canonicalize = False

        for pairs, reduction in canonicalize.items():
            pair1_idx = direction_to_idx[pairs[0]]
            pair2_idx = direction_to_idx[pairs[1]]
            reduction_idx = direction_to_idx[reduction] if reduction else None

            pair1_count = final_location[pair1_idx]
            pair2_count = final_location[pair2_idx]

            if pair1_count > 0 and pair2_count > 0:
                more_to_canonicalize = True

                if reduction_idx is None:  # opposing directions
                    num_to_cancel = min(pair1_count, pair2_count)
                    final_location[pair1_idx] = pair1_count - num_to_cancel
                    final_location[pair2_idx] = pair2_count - num_to_cancel
                else:  # reductions
                    num_to_reduce = min(pair1_count, pair2_count)
                    final_location[reduction_idx] += num_to_reduce
                    final_location[pair1_idx] = pair1_count - num_to_reduce
                    final_location[pair2_idx] = pair2_count - num_to_reduce

    return final_location


if __name__ == "__main__":
    # need a way to index tiles and how many times they've been flipped
    # directions are: ne, nw, e, w, se, sw
    tile_flips = defaultdict(int)  # keyed by (e, se, sw, w, nw, ne) --> # of flips
    directions = parse_directions("day24_input.txt")

    for line, direction in enumerate(directions):
        canonical_direction = canonicalize_directions(direction)
        tile_flips[tuple(canonical_direction)] += 1
    # pprint.pprint(tile_flips)

    num_flips = 0
    for _, count in tile_flips.items():
        if count % 2 != 0:
            num_flips += 1
    print(num_flips)

    # print(canonicalize_directions(["e", "se", "w"]))
    # print(canonicalize_directions(["nw", "w", "sw", "e", "e"]))
