#!/usr/bin/env python
import numpy as np

file = 'example'
           
f = open(file,'r')
lines_input = list(f)

def convert(e):
    if (e=='#'):
        return -2
    if (e=='.'):
        return -1
    if (e=='^'):
        return 0
    if (e=='>'):
        return 1
    if (e=='v'):
        return 2
    if (e=='<'):
        return 3  

matrix = np.array([[convert(e) for e in line.rstrip()] for line in lines_input])
N, M = np.shape(matrix)

def go_north(point):
    return Point(point.x-1, point.y, 0)

def go_east(point):
    return Point(point.x, point.y+1, 1)

def go_south(point):
    return Point(point.x+1, point.y, 2)

def go_west(point):
    return Point(point.x, point.y-1, 3)

directions_map = {
0: go_north,
1: go_east, 
2: go_south,
3: go_west
}

class Point:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y
    
    def __repr__(self):  
        return "(% s, % s)" % (self.x, self.y)  

    def __str__(self):  
        return "(% s, % s)" % (self.x, self.y)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def in_matrix(self):
        return self.x in range(0, N) and self.y in range(0, M)

def travel(pt, matrix):
    loop = False
    travel_poses = {pt: [pt.direction]}

    while pt.in_matrix():
        new_pt = directions_map[pt.direction](pt)
        if not new_pt.in_matrix():
            break
        if (matrix[new_pt.x, new_pt.y] == -2):
            pt = directions_map[(pt.direction+1) % 4](pt)
        else:
            pt = new_pt
            
        if pt in travel_poses:
            if pt.direction in travel_poses[pt]:
                loop = True
                break
            travel_poses[pt].append(pt.direction)
        else:
            travel_poses[pt] = [pt.direction]
    return travel_poses, loop


x, y = np.where(matrix > -1)
init_pt = Point(x[0], y[0], matrix[x[0], y[0]])
travel_poses, loop = travel(init_pt, matrix)

res = len(travel_poses)
print("Part1", res)

res_part2 = 0
for pt in travel_poses:
    if (pt == init_pt):
        continue
    backup = matrix[pt.x, pt.y]
    matrix[pt.x, pt.y] = -2
    travel_poses, loop = travel(init_pt, matrix)
    if (loop):
        res_part2 += 1

    matrix[pt.x, pt.y] = backup
    
print("Part2", res_part2)
#1650 too low
    
    
    
    
