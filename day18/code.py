#!/usr/bin/env python
import numpy as np
import heapq
import matplotlib.pyplot as plt
from scipy.ndimage import label

file = 'input'
plot = True
f = open(file, 'r')
lines = list(f)

directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]

if file == 'example':
    N = 7
    nb_bits = 12
else:
    N = 71
    nb_bits = 1024


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heuristic_cost = 2*N - x - y

    def is_same_position(self, other):
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "(% s, % s)" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.x, self.y))

    def get_neighbors(self):
        points = []

        for step in directions:
            new_pt = Point(self.x + step[0], self.y + step[1])
            if not is_in_matrix(new_pt) or not is_valid(new_pt):
                continue
            new_cost = get_cost(self.x, self.y) + 1
            if get_cost(new_pt.x, new_pt.y) <= new_cost:
                continue
            set_cost(new_pt, new_cost)
            points.append(new_pt)
        return points

    def __eq__(self, other):
        cost = get_cost(self.x, self.y) + self.heuristic_cost
        other_cost = get_cost(other.x, other.y) + other.heuristic_cost
        return cost == other_cost

    def __lt__(self, other):
        cost = get_cost(self.x, self.y) + self.heuristic_cost
        other_cost = get_cost(other.x, other.y) + other.heuristic_cost
        return cost < other_cost

    def __le__(self, other):
        cost = get_cost(self.x, self.y) + self.heuristic_cost
        other_cost = get_cost(other.x, other.y) + other.heuristic_cost
        return cost <= other_cost

    def __gt__(self, other):
        cost = get_cost(self.x, self.y) + self.heuristic_cost
        other_cost = get_cost(other.x, other.y) + other.heuristic_cost
        return cost > other_cost

    def __ge__(self, other):
        cost = get_cost(self.x, self.y) + self.heuristic_cost
        other_cost = get_cost(other.x, other.y) + other.heuristic_cost
        return cost >= other_cost


blocks = set()
for index, line in enumerate(lines):
    if (index == nb_bits):
        break
    x, y = line.rstrip().split(",")
    blocks.add(Point(int(y), int(x)))

cost_matrix = N*N*np.ones((N, N), dtype=np.uint32)
cost_matrix[0, 0] = 0


def get_cost(x, y):
    return cost_matrix[x, y]


def set_cost(point, cost):
    cost_matrix[point.x, point.y] = cost


def is_valid(point):
    return point not in blocks


def is_in_matrix(point):
    return 0 <= point.x < N and 0 <= point.y < N


# Part1
end_pt = Point(N-1, N-1)
start_pt = Point(0, 0)
open_set = [start_pt]
heapq.heapify(open_set)

hash_set = set()
hash_set.add(hash(start_pt))

while (len(open_set) > 0):
    best_point = heapq.heappop(open_set)
    hash_set.remove(hash(best_point))

    if (best_point.is_same_position(end_pt)):
        break
    children = best_point.get_neighbors()
    for child in children:
        if not hash(child) in hash_set:
            heapq.heappush(open_set, child)
            hash_set.add(hash(child))
        else:
            heapq.heapify(open_set)

if plot:
    plt.figure()
    plt.imshow(cost_matrix, cmap='gray')

print("Part1", cost_matrix[N-1, N-1])


# Part 2
blocks_matrix = np.ones((N, N), dtype=np.uint8)

for index, line in enumerate(lines):
    x, y = line.rstrip().split(",")
    blocks_matrix[int(y), int(x)] = 0

    if (index >= nb_bits):
        labelled, _ = label(blocks_matrix)
        if labelled[0, 0] != labelled[N-1, N-1]:
            print("Res part2", x, y)
            break

if plot:
    plt.figure()
    plt.imshow(blocks_matrix, cmap='gray')
