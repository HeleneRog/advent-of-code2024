#!/usr/bin/env python
import numpy as np

file = 'input'

f = open(file, 'r')
lines = list(f)

matrix = np.array([[int(e) for e in line.rstrip()] for line in lines])
M, N = np.shape(matrix)

directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]


def in_matrix(pt):
    return 0 <= pt[0] < N and 0 <= pt[1] < M


def condition_part1(pt, height, points):
    return (in_matrix(pt) and matrix[pt[0], pt[1]] == height
            and pt not in points)


def condition_part2(pt, height, points):
    return in_matrix(pt) and matrix[pt[0], pt[1]] == height


def compute_next_points(points, target_height, condition):
    new_points = []
    for pt in points:
        for di, dj in directions:
            new_pt = [pt[0] + di, pt[1] + dj]
            if condition(new_pt, target_height, new_points):
                new_points.append(new_pt)
    return new_points


init_points = [[int(i), int(j)] for i, j in list(zip(*np.where(matrix == 0)))]

# Part1
res_part1 = 0
for pt in init_points:
    height = 0
    points = [pt]
    while (height < 9):
        height += 1
        points = compute_next_points(points, height, condition_part1)
    res_part1 += len(points)

print("Part1", res_part1)

# Part2
points = init_points
height = 0
while (height < 9):
    height += 1
    points = compute_next_points(points, height, condition_part2)

print("Part2", len(points))
