def find_first_invalid_number(numbers):
    preamble_size = 25

    for idx, number in enumerate(numbers[preamble_size:]):
        offset_number = preamble_size + idx
        prev_slice = numbers[offset_number - 25 : offset_number]
        if not find_pairs(prev_slice, number):
            return offset_number, number


def get_input(input_filename):
    with open(input_filename) as f:
        return [int(line.rstrip("\n")) for line in f]


def find_pairs(nums, target_sum):
    nums.sort()
    front_idx = 0
    back_idx = len(nums) - 1

    while front_idx < back_idx:
        front_num = nums[front_idx]
        back_num = nums[back_idx]
        sum = front_num + back_num

        if sum == target_sum:
            return front_num, back_num
        elif sum < target_sum:  # go higher, from front
            front_idx = front_idx + 1
        else:  # sum > target_sum, go lower from back
            back_idx = back_idx - 1

    return None


def find_contiguous_sum(target_sum, numbers):
    current_start = 0
    current_end = 1
    current_sum = sum(numbers[current_start : current_end + 1])

    while current_sum != target_sum:
        if current_sum < target_sum:  # less, so need to try adding a number
            current_end = current_end + 1
        else:  # over, so need to remove the top
            current_start = current_start + 1

        current_sum = sum(numbers[current_start : current_end + 1])

    return numbers[current_start : current_end + 1]


if __name__ == "__main__":
    numbers = get_input("day9_input.txt")
    offset_number, number = find_first_invalid_number(numbers)
    contiguous_numbers = find_contiguous_sum(number, numbers)
    print(min(contiguous_numbers) + max(contiguous_numbers))
