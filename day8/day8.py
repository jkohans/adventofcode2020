def find_infinite_loop(input_filename):
    instructions = []

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")
            parts = line.split(" ")
            num = int(parts[1][1:])
            if parts[1][0] == "-":
                num = -1 * num
            instructions.append((parts[0], int(num)))

    for permutation in get_permutations(instructions):
        print(permutation)
        next_instruction, accumulator = execute_instructions(permutation)
        # print(next_instruction, accumulator)
        if next_instruction == len(instructions):
            return next_instruction, accumulator


def get_permutations(instructions):
    # jmp and nop are swapped somehwere?
    for idx, instruction in enumerate(instructions):
        command, num = instruction
        if command == "jmp":
            yield instructions[:idx] + [("nop", num)] + instructions[idx + 1 :]
        elif command == "nop":
            yield instructions[:idx] + [("jmp", num)] + instructions[idx + 1 :]


def execute_instructions(instructions):
    instructions_visited = set()
    global_accumulator = 0
    next_instruction = 0

    while next_instruction not in instructions_visited and next_instruction < len(instructions):
        instructions_visited.add(next_instruction)
        instruction, num = instructions[next_instruction]

        if instruction == "acc":
            global_accumulator += num
            next_instruction = next_instruction + 1
        elif instruction == "nop":
            next_instruction = next_instruction + 1
        elif instruction == "jmp":
            next_instruction = next_instruction + num
        else:
            print("unknown instruction", instruction)
            exit(1)

    return next_instruction, global_accumulator


if __name__ == "__main__":
    instruction, accumulator = find_infinite_loop("day8_input.txt")
    print(accumulator)
