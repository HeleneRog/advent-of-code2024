#!/usr/bin/env python
import numpy as np
import copy

file = 'input'

f = open(file, 'r')
lines = list(f)


def condition_part_1(report):
    diff = np.diff(report)
    return (all(0 < x < 4 for x in diff) or all(-4 < x < 0 for x in diff))


def condition_part_2(report):
    for index, _ in enumerate(report):
        new_report = copy.copy(report)
        report.pop(index)
        if condition_part_1(new_report):
            return True
    return False


res = 0
res2 = 0

for line in lines:
    report = [int(e) for e in line.split()]
    res += condition_part_1(report)
    res2 += condition_part_2(report)


print("res part 1: ", res)
print("res part 2: ", res2)
