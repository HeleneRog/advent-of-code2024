#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label

file = 'input'

f = open(file,'r')
lines = list(f)

if file == 'example':
    N, M = 11, 7
else:
    N, M = 101, 103


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)
    
    def __repr__(self):  
        return "(% s, % s)" % (self.x, self.y)  

    def __str__(self):  
        return self.__repr__()
    
    def __rmul__(self, factor):
        return Point(factor * self.x, factor * self.y)   


class Robot:   
    def __init__(self, x, y, vx, vy):
        self.position = Point(x, y)
        self.speed = Point(vx, vy)
        
    def move(self, nb_steps):
        pt = self.position + nb_steps * self.speed
        return Point(pt.x % N, pt.y % M)

    def __repr__(self):  
        return "{% s, % s}" % (self.position, self.speed)  

    def __str__(self):  
        return self.__repr__()


def compute_quadrant(point):
    Mlim = (M-1) / 2
    Nlim = (N-1) / 2
    if (point.x < Nlim):
        if (point.y < Mlim):
            return 0
        if (point.y > Mlim):
            return 1
    if (point.x > Nlim):
        if (point.y < Mlim):
            return 2
        if (point.y > Mlim):
            return 3
    return -1
    

quadrants = {0: 0, 1: 0, 2: 0, 3: 0}
steps = 100
robots = list()

for line in lines:
    pos, vel = [[int(f) for f in e.split("=")[1].split(",")] for e in line.rstrip().split(" ")]
    robot = Robot(pos[0], pos[1], vel[0], vel[1])
    robots.append(robot)
    final_position = robot.move(steps)
    quad = compute_quadrant(final_position)
    if (quad > -1):
        quadrants[quad] += 1

res_part1 = 1
for e in quadrants.values():
    res_part1 *= e
    
print("Part1:", res_part1)

# Part2
path = "/home/helene/Work/advent-of-code2024/day14/images/"
for i in range(1, 10000):
    mat = np.zeros((M, N))

    for robot in robots:
        position = robot.move(i)
        mat[position.y, position.x] = 1
        
    labelled, nb_labels = label(mat)
    for lab in range(1, nb_labels+1):
        size = len(np.where(labelled == lab)[0])
        if size > 10:
            fig = plt.figure()
            plt.title("Iteration %s" %(i))
            plt.imshow(mat, cmap='gray')
            fig.savefig(path+str(i))
            plt.close(fig)
            break
