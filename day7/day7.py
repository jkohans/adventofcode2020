from collections import defaultdict


def find_outermost_colors(input_filename, color):
    rules = defaultdict(lambda: [])
    forward_rules = defaultdict(lambda: [])

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")
            parts = line.split(" ")
            outside_bag_name, inside_bags = unroll_rule(parts, rules)
            forward_rules[outside_bag_name] = inside_bags

    # from part 1
    # outermost_bags, _ = perform_bfs(rules, color)
    # return len(outermost_bags)
    _, running_sum = perform_bfs(forward_rules, color)
    return running_sum


def perform_bfs(rules, color):
    # BFS
    level = rules[color]
    running_sum = sum(int(count) for count, _ in level)  # for the outermost bag
    outermost_bags = set()

    while level:
        next_level = []
        print(level)

        for count, bag_name in level:
            outermost_bags.add(bag_name)

            if rules[bag_name]:  # not an outermost bag
                for target_bag_count, target_bag_name in rules[bag_name]:  # go up another parent
                    outermost_bags.add(target_bag_name)
                    flattened_bags_count = int(count) * int(target_bag_count)
                    next_level.append((flattened_bags_count, target_bag_name))
                    print(flattened_bags_count)
                    running_sum = running_sum + flattened_bags_count
        level = next_level

    return outermost_bags, running_sum


def unroll_rule(parts, rules):
    # { target: [(count, bag_name1), (count, bag_name2)]}
    idx = 0
    outside_bag_name = []
    inside_bags = []

    while parts[idx] != "contain":
        outside_bag_name.append(parts[idx])
        idx = idx + 1
    outside_bag_name = " ".join(outside_bag_name[:-1])  # discard bag literal

    # unroll bag count
    idx = idx + 1  # advance past contain
    while idx < len(parts):
        if parts[idx] == "no":  # contains no other bags.
            break

        count = parts[idx]
        idx = idx + 1  # advance past count
        next_inside_bag_name = []

        # unroll bag name
        # example: 5 dotted white bags, 2 wavy lavender bags.
        while parts[idx][-1] not in [",", "."]:
            next_inside_bag_name.append(parts[idx])
            idx = idx + 1

        next_inside_bag_name = " ".join(next_inside_bag_name)
        rules[next_inside_bag_name].append((count, outside_bag_name))
        inside_bags.append((count, next_inside_bag_name))
        idx = idx + 1

    return outside_bag_name, inside_bags


if __name__ == "__main__":
    print(find_outermost_colors("day7_input.txt", "shiny gold"))
