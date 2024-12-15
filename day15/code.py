#!/usr/bin/env python
import numpy as np

file = 'input'
           
f = open(file,'r')
lines_input = list(f)

def convert_mat_element(e):
    if (e=='.'):
        return 0
    if (e=='O'):
        return 1
    if (e=='#'):
        return 3
    if (e=='@'):
        return 4


def convert_travel_element(e):
    if (e=='^'):
        return 0
    if (e=='>'):
        return 1
    if (e=='v'):
        return 2
    if (e=='<'):
        return 3


separator = lines_input.index("\n")
matrix = np.array([[convert_mat_element(e) for e in line.rstrip()] for line in lines_input[0:separator]])

travel = [convert_travel_element(e) for line in lines_input[separator+1:] for e in line.rstrip()]


def go_north(point):
    return Point(point.x-1, point.y)

def go_east(point):
    return Point(point.x, point.y+1)

def go_south(point):
    return Point(point.x+1, point.y)

def go_west(point):
    return Point(point.x, point.y-1)

directions_map = {
0: go_north,
1: go_east, 
2: go_south,
3: go_west
}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y
    
    def __repr__(self):  
        return "(% s, % s)" % (self.x, self.y)  

    def __str__(self):  
        return self.__repr__()
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def element(self):
        return matrix[self.x, self.y]


def set_free(point):
    matrix[point.x, point.y] = 0
    

def set_object(point):
    matrix[point.x, point.y] = 1


def is_wall(point):
    return (matrix[point.x, point.y] == 3)


def is_object(point):
    return (matrix[point.x, point.y] == 1)


def is_free(point):
    return (matrix[point.x, point.y] == 0)


def push_block(init_pt, direction):
    pt = init_pt
    while is_object(pt):
        pt = directions_map[direction](pt)
        
    if is_wall(pt):
        return False
    
    set_free(init_pt)
    set_object(pt)
    return True


def compute_next_point(point, direction):
    new_pt = directions_map[direction](point)
    if is_wall(new_pt):
        return point
    if is_free(new_pt):
        return new_pt
    succ = push_block(new_pt, direction)
    if succ:
        return new_pt
    return point


def compute_result():
    blocks = np.where(matrix == 1)
    positions = list(zip(*blocks))
    return sum([100 * x + y for x, y in positions])


x, y = np.where(matrix == 4)
point = Point(x[0], y[0])
set_free(point)

for direction in travel:
    point = compute_next_point(point, direction)


print("Part1", compute_result())

    
    
    
