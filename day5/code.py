#!/usr/bin/env python
from functools import cmp_to_key

file_results = 'input'

f = open(file_results,'r')
lines = list(f)

rules_succ = dict()
seqs = list()

part1 = True
for line in lines:
    if line == "\n":
        part1 = False
        continue
    if part1:
        pred, succ = [int(e) for e in line.rstrip().split("|")]
        if succ in rules_succ:
            rules_succ[succ].append(pred)
        else:
            rules_succ[succ] = [pred]
    else:
        seqs.append([int(e) for e in line.rstrip().split(",")])

def compare(a, b):
    if a in rules_succ and b in rules_succ[a]:
        return 1
    if b in rules_succ and a in rules_succ[b]:
        return -1
    return 0

def compute_res(seq):
    N = len(seq)
    return seq[int(N/2)]
        
res = 0
res_part2 = 0

for seq in seqs:
    sorted_seq = sorted(seq, key=cmp_to_key(compare))
    if seq == sorted_seq:
        res += compute_res(seq)
    else:
        res_part2 += compute_res(sorted_seq)
                
print("Part1", res)
print("Part2", res_part2)

    
    
    
    
