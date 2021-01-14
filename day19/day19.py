def parse_input(input_filename):
    section = 0
    rules = {}
    messages = []

    with open(input_filename) as f:
        for line in f:
            if line == "\n":
                section = section + 1
                continue

            line = line.rstrip("\n")
            if section == 0:  # parsing rules
                tokens = line.split(": ")
                index = tokens[0]

                options = tokens[1].split(" | ")

                # if len(options) == 1 and options[0].startswith("\""):
                #     rules[index] = [options[0]]  # probably can just be handled below?
                # else:
                patterns = []
                for option in options:
                    patterns.append(option.split())  # split the digit options

                rules[index] = patterns
            elif section == 1:  # parsing messages
                messages.append(line)
            else:
                print("Invalid section", section)
                exit(1)

    return rules, messages


def has_more_rules_to_follow(options_to_follow):
    for option in options_to_follow:
        for item in option:
            if not item.startswith('"'):  # there is still at least one number to follow
                return True

    return False


def collapse(final_options):
    collapsed = set()

    for option in final_options:
        collapsed.add("".join([letter[1:-1] for letter in option]))  # lop off the surrounding quotes

    return collapsed


def possible_messages_for_rule(rules, rule_number):
    options_to_follow = rules[rule_number]  # list of list of numbers

    while has_more_rules_to_follow(options_to_follow):
        print(len(options_to_follow))
        next_options_to_follow = []

        for option in options_to_follow:  # iterate over each option
            expanded_options = [[]]
            for maybe_index in option:  # iterate over each item in an option
                if maybe_index.startswith('"'):  # this is a terminal letter
                    for expanded_option in expanded_options:
                        expanded_option.append(maybe_index)
                else:  # this is a reference to a rule
                    next_rule = rules[maybe_index]

                    next_expanded_options = []  # grow the expanded options

                    for next_option in next_rule:
                        for expanded_option in expanded_options:
                            next_expanded_options.append(expanded_option + next_option)
                    expanded_options = next_expanded_options
            next_options_to_follow.extend(expanded_options)

        options_to_follow = next_options_to_follow

    return collapse(options_to_follow)


def find_matches(message, forty_two, thirty_one):
    return inner_find_matches(message, forty_two, thirty_one, [])


def inner_find_matches(message, forty_two, thirty_one, match_tracking):
    result = []

    if not message:
        return match_tracking

    for option_42 in forty_two:
        if message.startswith(option_42):
            remaining_message = message[len(option_42) :]
            next_match_tracking = match_tracking + [(option_42, 42, remaining_message)]
            result = result + inner_find_matches(remaining_message, forty_two, thirty_one, next_match_tracking)

    for option_31 in thirty_one:
        if message.startswith(option_31):
            remaining_message = message[len(option_31) :]
            next_match_tracking = match_tracking + [(option_31, 31, remaining_message)]
            result = result + inner_find_matches(remaining_message, forty_two, thirty_one, next_match_tracking)

    return result


def sequence_matches_pattern(sequence):
    # count 31s at the end and make sure there and at least n+1 42s at the beginning
    num_trailing_31s = 0

    for i in range(len(sequence) - 1, -1, -1):
        if sequence[i] == 31:
            num_trailing_31s += 1
        else:
            break

    if len(sequence) < num_trailing_31s * 2 + 1:
        # not enough numbers to make the pattern
        return False

    end_mid_idx = len(sequence) - num_trailing_31s
    front_mid_idx = end_mid_idx - num_trailing_31s
    mid_slice = sequence[front_mid_idx:end_mid_idx]
    front_slice = sequence[:front_mid_idx]

    if set(mid_slice) == {42} and set(front_slice) == {42}:
        return True
    else:
        return False


if __name__ == "__main__":
    rules, messages = parse_input("day19_input.txt")
    # rules is dict[index] -> [[1,2],[2,3]] or "a" directly
    # print(rules, messages)
    # possible_messages = possible_messages_for_rule(rules, "0")
    # print(possible_messages)
    # print(sum(1 for message in messages if message in possible_messages))

    # 0: 8 11 --> 42+ 42+n 31+n
    # rule 8 is 42+
    # rule 11 is 42+n 31+n, where n is the same
    forty_two = possible_messages_for_rule(rules, "42")
    thirty_one = possible_messages_for_rule(rules, "31")

    num_pattern_matches = 0
    for message in messages:
        match_tracking = find_matches(message, forty_two, thirty_one)
        sequence = [num for option, num, remaining, in match_tracking]  # this really should be a list of lists?
        if sequence_matches_pattern(sequence):
            num_pattern_matches += 1
        else:
            print("nope", message)
    print(num_pattern_matches)
