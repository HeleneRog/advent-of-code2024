#!/usr/bin/env python

file = 'input'

f = open(file, 'r')
lines = list(f)

A = int(lines[0].split(":")[1].rstrip())
B = int(lines[1].split(":")[1].rstrip())
C = int(lines[2].split(":")[1].rstrip())
program = [int(e) for e in lines[4].rstrip().split(":")[1].split(",")]
combo = {0: 0, 1: 1, 2: 2, 3: 3, 4: A, 5: B, 6: C}


def xor(lhs, rhs):
    return lhs ^ rhs


def adv(arg):
    combo[4] = int(combo[4] / 2**combo[arg])
    return False, None


def bxl(arg):
    combo[5] = xor(combo[5], arg)
    return False, None


def bst(arg):
    combo[5] = combo[arg] % 8
    return False, None


def jnz(arg):
    if (combo[4] == 0):
        return False, None
    return True, arg


def bxc(arg):
    combo[5] = xor(combo[5], combo[6])
    return False, None


def out(arg):
    return False, combo[arg] % 8


def bdv(arg):
    combo[5] = int(combo[4] / 2**combo[arg])
    return False, None


def cdv(arg):
    combo[6] = int(combo[4] / 2**combo[arg])
    return False, None


funcs = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc,
         5: out, 6: bdv, 7: cdv}


def solve():
    pointer = 0
    res = []
    while (pointer < len(program)):
        func_index = program[pointer]
        operand = program[pointer+1]
        jump, value = funcs[func_index](operand)

        if jump:
            pointer = value
        else:
            pointer += 2
        if not jump and value is not None:
            res.append(value)

    return res


res = solve()
res_str = "".join([str(e)+',' for e in res])
print("res part 1: ", res_str)


def solve_part2(x, expected_output):
    combo[4] = x
    combo[5] = 0
    combo[6] = 0

    pointer = 0
    output = 0

    while (pointer < len(program)):
        func_index = program[pointer]
        operand = program[pointer+1]
        jump, value = funcs[func_index](operand)

        if jump:
            if output == expected_output:
                return True
            else:
                return False
        else:
            pointer += 2
        if not jump and value is not None:
            output = value

    return (output == expected_output)


def get_bin(x, n=3):
    return format(x, 'b').zfill(n)


binary_numbers = ['']
binary_list = list(map(get_bin, range(0, 2**3)))
size_prog = len(program)

for step in range(1, size_prog+1):
    expected_output = program[size_prog-step]
    next_binary_numbers = []
    for binary_part in binary_list:
        for bin_nb in binary_numbers:
            new_nb = bin_nb+binary_part
            res = solve_part2(int(new_nb, 2), expected_output)
            if res:
                next_binary_numbers.append(new_nb)
    binary_numbers = next_binary_numbers

print("res part2:", int(min(binary_numbers), 2))
