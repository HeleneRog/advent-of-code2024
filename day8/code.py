#!/usr/bin/env python
import numpy as np
from itertools import combinations

file = 'example'
           
f = open(file,'r')
lines_input = list(f)

symbols = set()
def list_symbols(e):
    if e != '.':
        symbols.add(e)
    return e

matrix = np.array([[list_symbols(e) for e in line.rstrip()] for line in lines_input])
N, M = np.shape(matrix)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y
    
    def __repr__(self):  
        return "(% s, % s)" % (self.x, self.y)  

    def __str__(self):  
        return "(% s, % s)" % (self.x, self.y)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def in_matrix(self):
        return 0 <= self.x < N and 0 <= self.y < M
    
    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)
    
    def __neg__(self):
        return Point(-1 * self.x, -1 * self.y)        
    
    def __sub__(self, p):
        return self.__add__(-p)
    
    def __rmul__(self, factor):
        return Point(factor * self.x, factor * self.y)   

antinodes_part1 = set()
antinodes_part2 = set()

def add_to_set(pt, myset):
    if (pt.in_matrix()):
        myset.add(pt)

for symbol in symbols:
    positions = [Point(e[0], e[1]) for e in list(zip(*np.where(matrix == symbol)))]
    point_pairs = combinations(positions, 2)
    
    for p1, p2 in point_pairs:
        diff = p1 - p2
        
        for init_pt, sign in zip([p1, p2], [1, -1]):
            antinodes_part2.add(init_pt)
            antinode = init_pt + sign * diff
            add_to_set(antinode, antinodes_part1)
            add_to_set(antinode, antinodes_part2)

            while (antinode.in_matrix()):
                antinode = antinode + sign * diff
                add_to_set(antinode, antinodes_part2)
                

print("Part1", len(antinodes_part1))
print("Part2", len(antinodes_part2))
    
    
    
    
