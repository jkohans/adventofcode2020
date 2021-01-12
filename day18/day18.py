import re


def tokenize(input_filename):
    lines = []

    with open(input_filename) as f:
        for line in f:
            line = line.rstrip("\n")
            inner_tokens = [token for token in line.replace(" ", "")]
            lines.append(inner_tokens)

    return lines


def compute(lhs, rhs, op):
    result = 0

    if op == "+":
        result = lhs + rhs
    elif op == "*":
        result = lhs * rhs
    else:
        print("Encountered an invalid operator", op)
        exit(1)

    return result


def is_digit(token):
    return isinstance(token, int) or re.match("[0-9]", token)


def eval_expression(token_list):
    while len(token_list) > 1:
        token_queue = []

        # do successive iterations over the token list until there is only one number remaining
        while len(token_list):
            token = token_list.pop(0)

            if token in {"+", "*"}:
                # process a first expression
                if len(token_queue) == 1 and is_digit(token_queue[-1]) and is_digit(token_list[0]):
                    rhs = token_list.pop(0)  # pop the peeked item
                    token_queue = token_queue[:-1] + [compute(int(token_queue[-1]), int(rhs), token)]
                else:
                    token_queue.append(token)
            elif token == "(":
                # read until a matching closed paren and process entire expression
                inner_expression = []
                unmatched_parens = 1

                while unmatched_parens > 0:
                    token = token_list.pop(0)
                    if token == ")":
                        unmatched_parens -= 1
                    elif token == "(":
                        unmatched_parens += 1

                    inner_expression.append(token)
                token_queue.append(eval_expression(inner_expression[:-1]))  # discard the terminating ")"
            else:
                token_queue.append(token)

        token_list = token_queue

    return token_list[0]


if __name__ == "__main__":
    lines = tokenize("day18_input.txt")

    sum = 0
    for expression in lines:
        sum += eval_expression(expression)
    print(sum)

    # token_list = [token for token in "1+(2*3)+(4*(5+6))"]
    # token_list = [token for token in "1+(2*3)+(4*5+6)"]
    # token_list = "1 + 2 * 3 + 4 * 5 + 6".split()
    # token_list = [c for c in "((2+4*9)*(6+9*8+6)+6)+2+4*2"]
    # token_list = [c for c in "((2+4*9)*(6+9*8+6)+6)"]
    # print(eval_expression(token_list))
