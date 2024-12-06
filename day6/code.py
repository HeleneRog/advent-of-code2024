#!/usr/bin/env python
import numpy as np

file = 'input'
           
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

directions_map_bin = {
0: int('0001', 2),
1: int('0010', 2), 
2: int('0100', 2),
3: int('1000', 2)
}

def check_and_update_direction(current_direction, new_direction):
    if (current_direction == int('0000', 2)):
        return new_direction
    if (bin(current_direction & new_direction) != bin(current_direction)):
        return current_direction | new_direction
    else:
        return None


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
        return 0 <= self.x < N and 0 <= self.y < M


def compute_next_point(pt, matrix):
    new_pt = directions_map[pt.direction](pt)
    if not new_pt.in_matrix():
        return None
    while (matrix[new_pt.x, new_pt.y] == -2):
        new_pt = directions_map[(new_pt.direction+1) % 4](pt)
    if not new_pt.in_matrix():
        return None
    return new_pt


def travel(pt, matrix):
    loop = False
    travel_matrix = np.full((N, M), int('0000', 2))
    travel_matrix[pt.x, pt.y] = directions_map_bin[pt.direction]
    travel_poses = [pt]

    while pt.in_matrix():
        pt = compute_next_point(pt, matrix)
        if not pt:
            break
        new_dir = check_and_update_direction(travel_matrix[pt.x, pt.y],
                                             directions_map_bin[pt.direction])
        if not new_dir:
            loop = True
            break
        travel_matrix[pt.x, pt.y] = new_dir
        travel_poses.append(pt)
    return travel_poses, loop


x, y = np.where(matrix > -1)
init_pt = Point(x[0], y[0], matrix[x[0], y[0]])
travel_poses, _ = travel(init_pt, matrix)

res = len(set(travel_poses))
print("Part1", res)

res_part2 = 0
obstructions = set()
for index, pt in enumerate(travel_poses):
    if (pt == init_pt or pt in obstructions):
        continue
    obstructions.add(pt)
    matrix[pt.x, pt.y] = -2
    _, loop = travel(travel_poses[index-1], matrix)
    res_part2 += loop
    matrix[pt.x, pt.y] = -1
    
print("Part2", res_part2)
    
    
    
    
