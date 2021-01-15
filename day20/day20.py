from collections import Counter, defaultdict
import pprint


def parse_input(input_filename):
    tiles = dict()
    tile_num = None

    with open(input_filename) as f:
        next_tile = []

        for line in f:
            if line == "\n":
                tiles[tile_num] = next_tile
                next_tile = []
            else:
                line = line.rstrip("\n")

                if line.startswith("Tile"):
                    tile_num = line.split()[1][:-1]
                else:
                    next_tile.append([char for char in line])

    return tiles


def extract_frame(tile):
    # top, bottom, left, right
    return [tile[0], tile[-1], [row[0] for row in tile], [row[-1] for row in tile]]


def reverse(list_):
    return list(reversed(list_))


def identity(frame):
    return frame


def flip_top(frame):
    # top -> bottom, bottom -> top and sides are reversed
    return [frame[1], frame[0], reverse(frame[2]), reverse(frame[3])]


def flip_sides(frame):
    # left -> right, right -> left and top/bottom are reversed
    return [reverse(frame[0]), reverse(frame[1]), frame[3], frame[2]]


def rotate_90(frame):
    # top -> right, right + reverse -> bottom, bottom -> left, left + reverse -> top
    return [reverse(frame[2]), reverse(frame[3]), frame[1], frame[0]]


def rotate_180(frame):
    return rotate_90(rotate_90(frame))


def rotate_270(frame):
    return rotate_90(rotate_90(rotate_90(frame)))


def get_all_transformations(frame):
    transformations = []

    flip_transforms = [[identity], [flip_top], [flip_sides], [flip_top, flip_sides]]
    rotate_transforms = [identity, rotate_90, rotate_180, rotate_270]

    for flip in flip_transforms:
        for rotate in rotate_transforms:
            transformed_frame = frame.copy()
            for transform in flip + [rotate]:
                transformed_frame = transform(frame)
            transformations.append(transformed_frame)

    return transformations


def match_frames(frame, other_frame):
    matching_sides = []

    for i, side in enumerate(frame):
        for j, other_side in enumerate(other_frame):
            if side == other_side:
                matching_sides.append((i, j))

    return matching_sides


def find_matching_frame_shift(frame, other_frame):
    frame_transforms = get_all_transformations(frame)
    # other_frame_transforms = get_all_transformations(other_frame)

    for frame_shift in frame_transforms:
        # for other_frame_shift in other_frame_transforms:
        matching_sides = match_frames(frame_shift, other_frame)
        if matching_sides:
            return True

    return False


if __name__ == "__main__":
    tiles = parse_input("day20_input.txt")
    pprint.pprint(tiles)

    tiles_matching = Counter()

    for tile_num, tile in tiles.items():
        for other_tile_num, other_tile in tiles.items():
            if tile_num == other_tile_num:
                continue  # can't match a tile with itself

            frame = extract_frame(tile)
            other_frame = extract_frame(other_tile)

            # don't have to worry about tracking which orientation was used up
            # bc it looks like frames uniquely match with one another?
            if find_matching_frame_shift(frame, other_frame):
                tiles_matching[tile_num] += 1

    num = 1
    for tile_num, matching_sides in tiles_matching.items():
        if matching_sides == 2:
            print(tile_num, "has", matching_sides, "matching sides")  # to sanity check that there's only 4 in the data
            num = num * int(tile_num)
    print(num)
