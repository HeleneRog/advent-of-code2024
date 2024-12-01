#!/usr/bin/env python

file_results = 'example'

f = open(file_results,'r')
lines = list(f)

left_values, right_values = zip(*[[int(e) for e in line.split()] for line in lines])

# Part 1
res = 0
for a,b in zip(sorted(left_values), sorted(right_values)):
    res += abs(a-b)

print("res part 1: ", res)

# Part 2
res2 = 0
for e in left_values:
    res2 += e * right_values.count(e)
    
print("res part 2: ", res2)
