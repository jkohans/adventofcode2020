from collections import Counter, defaultdict, namedtuple
import pprint


Pane = namedtuple("Pane", ["this", "top", "bottom", "left", "right"])


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
    # top, right, bottom, left
    return [tile[0], [row[-1] for row in tile], tile[-1], [row[0] for row in tile]]


def reverse(list_):
    return list(reversed(list_))


def identity(tile):
    return tile


def flip_top(tile):
    # reverse rows
    return reverse(tile)


def flip_sides(tile):
    # reverse columns
    return [reverse(row) for row in tile]


def rotate_90(tile):
    rotated = []

    # turn rows to columns + reverse
    for row in tile:
        for i, cell in enumerate(row):  # i is column number
            if i >= len(rotated):
                rotated.append([cell])
            else:
                rotated[i].append(cell)

    return flip_sides(rotated)


def rotate_180(frame):
    return rotate_90(rotate_90(frame))


def rotate_270(frame):
    return rotate_90(rotate_90(rotate_90(frame)))


def rotate_counter90(tile):
    rotated = []

    # turn rows to columns + flip_top
    for row in tile:
        for i, cell in enumerate(row):  # i is column number
            if i >= len(rotated):
                rotated.append([cell])
            else:
                rotated[i].append(cell)

    return flip_top(rotated)


def rotate_counter180(tile):
    return rotate_counter90(rotate_counter90(tile))


def rotate_counter270(tile):
    return rotate_counter90(rotate_counter90(rotate_counter90(tile)))


def get_all_transformations(tile):
    transformations = []

    # there are probably some redundant transformations here too, but they won't affect correctness
    flip_transforms = [[identity], [flip_top], [flip_sides], [flip_top, flip_sides]]
    rotate_transforms = [
        identity,
        rotate_90,
        rotate_180,
        rotate_270,
        rotate_counter90,
        rotate_counter180,
        rotate_counter270,
    ]

    for flip in flip_transforms:
        for rotate in rotate_transforms:
            transformed_tile = tile
            for transform in flip + [rotate]:
                transformed_tile = transform(transformed_tile)
            transformations.append(transformed_tile)

    return transformations


def match_sides(tile, other_tile):
    matching_sides = []
    frame = extract_frame(tile)
    other_frame = extract_frame(other_tile)

    for i, side in enumerate(frame):
        for j, other_side in enumerate(other_frame):
            if side == other_side:
                matching_sides.append((i, j))

    return matching_sides


def find_matching_side(tile, other_tile):
    matches = []
    transforms = get_all_transformations(other_tile)

    for transform in transforms:
        matching_sides = match_sides(tile, transform)
        if matching_sides:
            matches.append((transform, matching_sides))

    return matches


def find_top_left(image_spec):
    # navigate to top-left of image and then draw it out...
    _, pointer_pane = list(image_spec.items())[0]  # num, pane

    while pointer_pane.top:
        pointer_pane = image_spec[pointer_pane.top[0]]

    while pointer_pane.left:
        pointer_pane = image_spec[pointer_pane.left[0]]

    return pointer_pane


def assemble_rows(super_tiles):
    assembled = []

    for tile in super_tiles:
        for row in tile:
            assembled.append(row)

    return assembled


def paste_rows(tiles):
    pasted = []

    for i in range(len(tiles[0])):  # iterate over the rows
        for tile in tiles:
            if i >= len(pasted):
                pasted.append(tile[i])
            else:
                pasted[i].extend(tile[i])

    return pasted


def assemble_image(image_spec):
    top_left = find_top_left(image_spec)
    walker = top_left
    super_tiles = []

    while True:  # walking down
        side_walker = walker
        tiles = [remove_borders(side_walker.this[1])]
        print("walking down from...", side_walker.this[0])

        while side_walker.right:  # walking across
            tile_num, tile = side_walker.right
            print("walking right from...", tile_num)
            tiles.append(remove_borders(tile))
            side_walker = image_spec[tile_num]

        super_tiles.append(paste_rows(tiles))

        if not walker.bottom:  # arrived at the bottom of the image
            break

        walker = image_spec[walker.bottom[0]]

    return assemble_rows(super_tiles)


def pick_match(matches):
    # top, right, bottom, left
    # 0->2, 1->3, 2->0, 3->1, match up top<->bottom and left<->right
    pairs = {0: 2, 1: 3, 2: 0, 3: 1}

    tile, matching_sides = matches[0]
    matching_side = matching_sides[0]
    target_sides = (matching_side[0], pairs[matching_side[0]])  # the pairing of sides to find

    for tile, matching_sides in matches:
        matching_side = matching_sides[0]
        if matching_side == target_sides:
            return tile, matching_side

    print("Something terrible happened...")
    exit(1)


def remove_borders(tile):
    trimmed = []

    for i, row in enumerate(tile):
        if i not in {0, len(tile) - 1}:
            trimmed_row = []
            for j, column in enumerate(row):
                if j not in {0, len(row) - 1}:
                    trimmed_row.append(column)
            trimmed.append(trimmed_row)

    return trimmed


def extract_tile(image, rows, position, length):
    tile = []

    for i in range(rows[0], rows[1]):
        row = []
        for j in range(position, position + length):
            row.append(image[i][j])
        tile.append(row)

    return tile


def extract_fingerprint(image):
    coords = set()

    for i, row in enumerate(image):
        for j, column in enumerate(row):
            if column == "#":
                coords.add((i, j))

    return coords


def find_seamonsters(image, seamonster_coords):
    num_seamonsters_found = 0
    rows = (0, 3)

    # scan for the seamonster
    while rows[1] <= len(image):
        position = 0
        monster_length = len(seamonster[0])

        while position <= len(image[0]) - monster_length:
            # is there a seamonster here?
            tile = extract_tile(image, rows, position, monster_length)
            tile_fingerprint = extract_fingerprint(tile)

            if seamonster_coords.issubset(tile_fingerprint):
                num_seamonsters_found += 1
            position = position + 1
        rows = (rows[0] + 1, rows[1] + 1)

    return num_seamonsters_found


def count_pixels(image):
    num_pixels = 0

    for row in image:
        for column in row:
            if column == "#":
                num_pixels += 1

    return num_pixels


if __name__ == "__main__":
    tiles = parse_input("day20_input.txt")
    # pprint.pprint(tiles)

    tiles_matching = Counter()

    frontier = [list(tiles.items())[0]]
    image_spec = {}
    seen_tiles = set()

    while frontier:
        next_frontier = []

        for tile_num, tile in frontier:
            if tile_num in seen_tiles:  # avoid cycles
                continue

            top = None  # 0
            right = None  # 1
            bottom = None  # 2
            left = None  # 3

            for other_tile_num, other_tile in tiles.items():
                if tile_num == other_tile_num:  # a tile cannot match sides with itself
                    continue

                # print("comparing tiles", tile_num, other_tile_num)
                matches = find_matching_side(tile, other_tile)

                if matches:
                    other_transform, matching_side = pick_match(matches)
                    side, other_side = matching_side

                    if side == 0:
                        top = (other_tile_num, other_transform)
                    elif side == 1:
                        right = (other_tile_num, other_transform)
                    elif side == 2:
                        bottom = (other_tile_num, other_transform)
                    else:
                        left = (other_tile_num, other_transform)

                    if other_tile_num not in seen_tiles:  # avoid cycles
                        next_frontier.append((other_tile_num, other_transform))

            seen_tiles.add(tile_num)

            image_spec[tile_num] = Pane(this=(tile_num, tile), top=top, bottom=bottom, left=left, right=right)
        frontier = next_frontier

    # for tile_num, pane in image_spec.items():
    #     count = 0
    #     if pane.top is not None:
    #         count += 1
    #     if pane.bottom is not None:
    #         count += 1
    #     if pane.left is not None:
    #         count += 1
    #     if pane.right is not None:
    #         count += 1
    #     tiles_matching[count] += 1
    #
    # print(tiles_matching.most_common())  # sanity check number of sides for each tile

    image = assemble_image(image_spec)
    print(len(image), "x", len(image[0]))
    pprint.pprint(image, width=1000)

    seamonster = [list("                  # "), list("#    ##    ##    ###"), list(" #  #  #  #  #  #   ")]
    seamonster_coords = extract_fingerprint(seamonster)

    for transform in get_all_transformations(image):
        num_monsters_found = find_seamonsters(transform, seamonster_coords)
        print(num_monsters_found)
        if num_monsters_found:
            print("found:", num_monsters_found)
            print(count_pixels(transform) - len(seamonster_coords) * num_monsters_found)
            break
