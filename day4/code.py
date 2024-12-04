#!/usr/bin/env python
import numpy as np

file_results = 'input'

f = open(file_results,'r')
lines = list(f)

def convert(c):
    if c == 'X':
        return 0
    if c == 'M':
        return 1
    if c == 'A':
        return 2
    if c == 'S':
        return 3

    
matrix = [[convert(e) for e in line.rstrip()] for line in lines]
mat = np.array(matrix)
M, N = np.shape(mat) 

# Part1
res = 0
zeros = np.where(mat == 0)

for i, j in zip(*zeros):
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if (-1 < i+3*di < M and -1 < j+3*dj < N):
                if [mat[i+di, j+dj], mat[i+2*di, j+2*dj],  mat[i+3*di, j+3*dj]] == [1, 2, 3]:
                    res += 1
print("Part1", res)


#Part2
res_part2 = 0
A_list = np.where(mat == 2)

for i, j in zip(*A_list):
    if (i in [0, M-1] or j in [0, N-1]):
        continue
    if ((mat[i-1, j-1] * mat[i+1, j+1] == 3)
        and (mat[i-1, j+1] * mat[i+1, j-1] == 3)):
        res_part2 += 1

print("Part2", res_part2)

    
    
    
    
