from collections import defaultdict


def load_adapaters(input_filename):
    with open(input_filename) as f:
        return [int(line.rstrip("\n")) for line in f]


def get_differences(adapters):
    return [adapters[i] - adapters[i - 1] for i in range(1, len(adapters))]


def find_all_combos(adapters):
    combos = []
    _inner_find_all_combos([adapters[0]], adapters[1:], combos)
    return combos


def _inner_find_all_combos(current_chain, remaining_adapters, combos):
    if not remaining_adapters:
        combos.append(current_chain)
    else:
        jolt = current_chain[-1]
        next_idx = 0

        while next_idx < len(remaining_adapters) and jolt < remaining_adapters[next_idx] <= jolt + 3:
            next_chain = current_chain + [remaining_adapters[next_idx]]
            next_adapters = remaining_adapters[next_idx + 1 :]
            _inner_find_all_combos(next_chain, next_adapters, combos)
            next_idx = next_idx + 1


def count_overlaps(jolt, idx, adapters):
    next_idx = idx + 1
    overlaps = set()
    count = 0

    while next_idx < len(adapters) and jolt < adapters[next_idx] <= jolt + 3:
        overlaps.add(adapters[next_idx])
        count = count + 1
        next_idx = next_idx + 1

    return count


def get_segments(adapters):
    overlaps_at_idx = []

    for idx, jolt in enumerate(adapters):
        count = count_overlaps(jolt, idx, adapters)
        overlaps_at_idx.append(count)

    current_segment = []

    for idx, jolt in enumerate(adapters):
        overlap_count = overlaps_at_idx[idx]

        if overlap_count == 1:
            if len(current_segment) >= 2:
                if overlaps_at_idx[idx - 2 : idx - 1 + 1] in ([2, 1], [1, 1]):  # hit a 211 or 111 breaker
                    current_segment.append(jolt)
                    yield current_segment
                    current_segment = []
                else:
                    current_segment.append(jolt)
            elif set(current_segment) not in [set(), {1}]:  # not a string of 1s
                current_segment.append(jolt)
        elif overlap_count == 2:
            current_segment.append(jolt)
        elif overlap_count == 3:
            current_segment.append(jolt)


if __name__ == "__main__":
    adapters = load_adapaters("input_day10.txt")
    adapters.sort()
    adapters = [0] + adapters + [adapters[-1] + 3]
    print(adapters)
    segments = get_segments(adapters)

    num_combinations = 1

    for segment in segments:
        combos = find_all_combos(segment)
        num_combinations = num_combinations * len(combos)
    print(num_combinations)

    # part 1
    # differences = get_differences(adapters)
    # frequencies = defaultdict(int)
    # for difference in differences:
    #     frequencies[difference] = frequencies[difference] + 1
    #
    # print(frequencies[1] * frequencies[3])
