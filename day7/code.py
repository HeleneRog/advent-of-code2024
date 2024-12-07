#!/usr/bin/env python

file = 'example'
           
f = open(file,'r')
lines_input = list(f)


def compute_part1(res, number):
    return [res + number, res * number]

def compute_part2(res, number):
    return [res + number, res * number, int(str(res) + str(number))]

def try_combinatory(result, numbers, func):
    results = [numbers[0]]
    
    for nb in numbers[1:]:
        new_results = []
        for res in results:
            new_results.extend(func(res, nb))
        results = new_results
    
    return result in results

res_part1 = 0
res_part2 = 0

for line in lines_input:
    result, numbers = line.rstrip().split(":")
    result = int(result)
    number_list = [int(e) for e in numbers.split()]
    
    if (try_combinatory(result, number_list, compute_part1)):
        res_part1 += result
    if (try_combinatory(result, number_list, compute_part2)):
        res_part2 += result
        
print("Part1:", res_part1)
print("Part2:", res_part2)
