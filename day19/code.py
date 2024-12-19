#!/usr/bin/env python
import re

file = 'input'

f = open(file, 'r')
lines = list(f)

patterns = [e for e in lines[0].rstrip().split(", ")]

patterns_regex_list = []
regex = "\A("

for index, pattern in enumerate(patterns):
    regex += pattern
    patterns_regex_list.append("\A"+pattern)
    if (index < len(patterns) - 1):
        regex += "|"

regex += ")+\Z"

sizes_dict = {}


def find_combinations(line):
    if (line in sizes_dict):
        return sizes_dict[line]
    nb_combs = 0
    for pattern_reg in patterns_regex_list:
        subs = re.split(pattern_reg, line)
        if (len(subs) == 1):
            continue
        if (subs[1] == ''):
            nb_combs += 1
            continue
        nb_combs += find_combinations(subs[1])
    sizes_dict[line] = nb_combs
    return nb_combs


nb_valid_lines = 0
nb_combinations = 0
for line in lines[2:]:
    x = re.search(regex, line.rstrip())
    if x:
        nb_valid_lines += 1
        nb_combinations += find_combinations(line.rstrip())

# Part 1
print("res part 1: ", nb_valid_lines)
print("res part 2: ", nb_combinations)
