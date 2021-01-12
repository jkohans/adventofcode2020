def get_manhattan_distance(input_filename):
    rotations = ["N", "E", "S", "W"]  # 90 degrees positive
    # direction_to_idx = {
    #     'N': 0,
    #     'E': 1,
    #     'S': 2,
    #     'W': 3
    # }
    # current_direction_idx = 1
    totals = [0, 0, 0, 0]  # NESW

    # 10 east, 1 north
    waypoint = [1, 10, 0, 0]

    # NSEW moves waypoint
    # L rotate waypoint counter-clockwise around ship by # of degrees
    # R rotate waypoint clockwise around ship by # of degrees
    # F move toward the waypoint number of times

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")
            direction = line[0]
            # NSEW, Left, Right, Forward
            units = int(line[1:])

            if direction == "N":
                waypoint[0] += units
            elif direction == "E":
                waypoint[1] += units
            elif direction == "S":
                waypoint[2] += units
            elif direction == "W":
                waypoint[3] += units
            elif direction == "F":
                for i in range(len(totals)):
                    totals[i] += units * waypoint[i]
                # totals[current_direction_idx] += units
            elif direction == "R":
                # for every 90 degrees one turn
                # this and L only move the waypoint
                num_turns = int(units / 90)
                # current_direction_idx = (current_direction_idx + num_turns) % len(rotations)
                for _ in range(num_turns):
                    waypoint = [waypoint[3]] + waypoint[:3]
            elif direction == "L":
                num_turns = int(units / 90)
                # current_direction_idx = (current_direction_idx - num_turns) % len(rotations)
                for _ in range(num_turns):
                    waypoint = waypoint[1:] + [waypoint[0]]
            else:
                print("unknown direction", direction)
                exit(1)

            # print(waypoint)
            # print(totals)
            # print("-----")

    # N - S, E - W
    return abs(totals[0] - totals[2]), abs(totals[1] - totals[3])


if __name__ == "__main__":
    print(sum(get_manhattan_distance("input_day12.txt")))
