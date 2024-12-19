#!/usr/bin/env python
import re

file = 'example'

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


def find_combinations(line):
    nb_combs = 0
    for pattern_reg in patterns_regex_list:
        subs = re.split(pattern_reg, line)
        if (len(subs) == 1):
            continue
        if (subs[1] == ''):
            nb_combs += 1
            continue
        sub_combs = find_combinations(subs[1].rstrip())
        nb_combs += sub_combs
    return nb_combs


nb_sols = 0
total_sols = 0
for line in lines[2:]:
    x = re.search(regex, line.rstrip())
    if x:
        nb_sols += 1
        total_sols += find_combinations(line)

# Part 1
print("res part 1: ", nb_sols)
print("res part 2: ", total_sols)
