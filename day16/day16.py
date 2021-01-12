def parse_input(input_filename):
    section = 0
    rules = dict()
    my_ticket = []
    nearby_tickets = []

    with open(input_filename) as f:
        for line in f:
            if line == "\n":
                section = section + 1
            else:
                line = line.rstrip("\n")

                if section == 0:
                    parts = line.split(": ")
                    field = parts[0]
                    ranges = parts[1].split(" or ")
                    rules[field] = ranges
                elif section == 1:
                    if line == "your ticket:":  # skip it
                        continue
                    my_ticket = [int(num) for num in line.split(",")]
                elif section == 2:
                    if line == "nearby tickets:":  # skip it
                        continue
                    nearby_tickets.append([int(num) for num in line.split(",")])
                elif section == 3:
                    print("Encountered an extra section")
                    exit(1)

    return rules, my_ticket, nearby_tickets


def in_range(number, ranges):
    for range in ranges:
        min, max = range.split("-")
        min, max = int(min), int(max)

        if min <= number <= max:
            return True

    return False


# def solve_constraints(rules, valid_tickets, positions):
#     if not valid_tickets[0]:
#         return positions
#
#     first_values = [ticket[0] for ticket in valid_tickets]
#     for field, ranges in rules.items():  # try each rule out on all first values
#         if field in positions:  # this field has already been used
#             continue
#
#         rule_passes_all_vals = True
#         for val in first_values:
#             if not in_range(val, ranges):
#                 rule_passes_all_vals = False
#                 break
#
#         if rule_passes_all_vals:  # the rule passes for all values
#             next_positions = positions.copy()
#             next_positions.append(field)
#             result = solve_constraints(rules, [ticket[1:] for ticket in valid_tickets], next_positions)
#             if result:
#                 print(result)


def solve_constraints(rules, valid_tickets, _):
    options = []

    for i in range(len(valid_tickets[0])):
        field_slice = [field_values[i] for field_values in valid_tickets]
        inner_options = set()

        for field, ranges in rules.items():
            rule_passes_all_vals = True
            for val in field_slice:
                if not in_range(val, ranges):
                    rule_passes_all_vals = False
                    break
            if rule_passes_all_vals:
                inner_options.add(field)
        options.append(inner_options)

    final_position = [None for _ in range(len(valid_tickets[0]))]
    used_fields = set()
    coalesced = False

    while not coalesced:
        coalesced = True
        for position, inner_options in enumerate(options):
            diff = inner_options.difference(used_fields)
            if len(diff) == 1:
                final_field = next(iter(diff))
                final_position[position] = final_field
                used_fields.add(final_field)
                coalesced = False

    return final_position


if __name__ == "__main__":
    rules, my_ticket, nearby_tickets = parse_input("day16_input.txt")

    sum = 0
    valid_tickets = []
    all_tickets = nearby_tickets.copy()
    all_tickets.append(my_ticket)

    for ticket in all_tickets:
        is_valid_ticket = True
        for field_value in ticket:
            invalid = True
            for _, ranges in rules.items():
                if in_range(field_value, ranges):
                    invalid = False
            if invalid:
                sum = sum + field_value
                is_valid_ticket = False

        if is_valid_ticket:
            valid_tickets.append(ticket)

    final_position = solve_constraints(rules, valid_tickets, [])
    product = 1
    for i, field in enumerate(final_position):
        if field.startswith("departure"):
            product = product * my_ticket[i]
    print(product)
