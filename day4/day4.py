import re


def count_passports(input_file):
    fields = dict()
    valid_count = 0

    for line in open(input_file, "r"):
        if line == "\n":  # finished unrolling a passport
            if check_valid(fields):
                valid_count = valid_count + 1
            # print(fields)
            fields = dict()  # reset fields
        else:
            for pairs in line.rstrip("\n").split(" "):
                key, value = pairs.split(":")
                fields[key] = value

    # print(fields)
    if check_valid(fields):
        valid_count = valid_count + 1

    return valid_count


def check_valid(fields):
    def validate_height(hgt):
        if re.search("^\d{3}cm$", hgt):
            number = hgt[: len(hgt) - 2]
            return 150 <= int(number) <= 193
        elif re.search("^\d{2}in$", hgt):
            number = hgt[: len(hgt) - 2]
            return 59 <= int(number) <= 76
        else:
            return False

    passport_validators = {
        "byr": lambda x: re.search("^\d{4}$", x) and 1920 <= int(x) <= 2002,
        "iyr": lambda x: re.search("^\d{4}$", x) and 2010 <= int(x) <= 2020,
        "eyr": lambda x: re.search("^\d{4}$", x) and 2020 <= int(x) <= 2030,
        "hgt": validate_height,
        "hcl": lambda x: re.search("^#[0-9a-f]{6}$", x),
        "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
        "pid": lambda x: re.search("^\d{9}$", x),
        "cid": lambda x: True,
    }

    north_pole_creds_validators = passport_validators.copy()
    del north_pole_creds_validators["cid"]

    if set(fields.keys()) in [passport_validators.keys(), north_pole_creds_validators.keys()]:
        is_valid = True
        for key, value in fields.items():
            is_valid = is_valid and passport_validators[key](value)
        # print("one or the other")
        # print(fields.keys(), "of size", len(fields.keys()))
        return is_valid
    else:
        # print("neither")
        # print(fields.keys(), "of size", len(fields.keys()))
        return False


if __name__ == "__main__":
    num_valid = count_passports("input2.txt")
    print(num_valid)
