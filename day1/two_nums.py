def find_solution(filename):
    nums = load_nums(filename)
    nums.sort()
    front_idx = 0
    back_idx = len(nums) - 1

    while front_idx != back_idx:
        front_num = nums[front_idx]
        back_num = nums[back_idx]
        sum = front_num + back_num

        if sum == 2020:
            print(front_num, back_num, front_num * back_num)
            break
        elif sum < 2020:  # go higher, from front
            front_idx = front_idx + 1
        else:  # sum > 2020, go lower from back
            back_idx = back_idx - 1


def load_nums(filename):
    nums = [int(i) for i in open(filename, "r")]
    nums.sort()
    return nums


def find_solution3(filename):
    nums = load_nums(filename)
    nums_set = set(nums)
    nums.sort()
    front_idx = 0
    back_idx = len(nums) - 1

    while front_idx != back_idx:
        front_num = nums[front_idx]
        back_num = nums[back_idx]
        sum = front_num + back_num

        difference = 2020 - sum
        if difference in nums_set:
            print(front_num, back_num, difference, front_num * back_num * difference)
            break
        elif difference > 0:  # go higher, from front
            front_idx = front_idx + 1
        else:  # difference is negative, go lower from back
            back_idx = back_idx - 1


# anonymous user #1258239
if __name__ == "__main__":
    # find_solution("advent_day1.txt")
    find_solution3("advent_day1.txt")
