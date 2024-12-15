#!/usr/bin/env python
import re

file = 'input'

f = open(file, 'r')
line = f.read()


def compute_mul(line):
    sequences = re.findall("mul\([0-9]+,[0-9]+\)", line)
    res = 0
    for seq in sequences:
        a, b = [int(e) if int(e) <
                1000 else 0 for e in re.findall("[0-9]+", seq)]
        res += a*b
    return res


# Part 1
print("res part 1: ", compute_mul(line))


# Part 2
split_dont = re.split("don't()", line)
res2 = compute_mul(split_dont[0])

for split_dont_element in split_dont[1:]:
    if not split_dont_element:
        continue
    split_do = re.split("do()", split_dont_element)
    for seq in split_do[1:]:
        res2 += compute_mul(seq)

print("res part 2: ", res2)
