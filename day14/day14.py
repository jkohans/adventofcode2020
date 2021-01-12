def get_values_in_memory(input_filename):
    memory = dict()

    with open(input_filename) as f:
        current_mask = None

        for line in f:
            line = line.rstrip("\n")

            if line.startswith("mask"):
                mask = line.split(" = ")[1]
                current_mask = mask
            elif line.startswith("mem"):
                parts = line.split(" = ")
                address = parts[0]
                address = int(address[4 : len(address) - 1])
                value = int(parts[1])

                masked_addresses = get_masked_values(address, current_mask)
                for masked in masked_addresses:
                    memory[masked] = value

                # memory[address] = get_masked_value(value, current_mask)  # part 1

    return memory


def bitstring_to_int(bitstring):
    return int(bitstring, 2)


def int_to_bitstring(int_):
    bitstring = "{0:036b}".format(int_)
    return bitstring


def get_floating_values(bitstring):
    current_values = [""]

    for bit in bitstring:
        next_values = []

        if bit in {"0", "1"}:
            next_values = [value + bit for value in current_values]
        else:  # X
            for value in current_values:
                next_values.append(value + "0")
                next_values.append(value + "1")

        current_values = next_values

    return current_values


def get_masked_values(value, mask):
    bitstring = int_to_bitstring(value)

    result = ""
    for idx, char in enumerate(mask):
        if char == "0":
            result += bitstring[idx]
        elif char == "1":
            result += "1"
        elif char == "X":
            result += "X"

    results = get_floating_values(result)

    return map(bitstring_to_int, results)


if __name__ == "__main__":
    memory = get_values_in_memory("day14_input.txt")

    sum = 0
    for key, value in memory.items():
        sum += value
    print(sum)
