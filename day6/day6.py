def find_sum(input_filename):
    group_answers = []
    unique_results = []

    for line in open(input_filename):
        line = line.rstrip("\n")
        if line == "":  # gathered a complete group
            uniques = analyze_uniques(group_answers)
            unique_results.append(uniques)
            group_answers = []
        else:
            line = line.rstrip("\n")
            group_answers.append(line)

    # and one last one for end of file
    uniques = analyze_uniques(group_answers)
    unique_results.append(uniques)

    return sum(len(uniques) for uniques in unique_results)


def analyze_uniques(group_answers):
    result = set(group_answers[0])

    for answer in group_answers:
        result = result.intersection(set(item for item in answer))

    return result


if __name__ == "__main__":
    result = find_sum("day6_input.txt")
    print(result)
