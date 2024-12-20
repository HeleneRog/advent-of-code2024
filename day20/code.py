#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

file = 'input'
save_duration_thres = 100
max_cheat_distance = 20

plot = False

f = open(file, 'r')
lines = list(f)

directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]


def convert_mat_element(e):
    if (e == '.'):
        return 1
    if (e == '#'):
        return 0
    if (e == 'S'):
        return 2
    if (e == 'E'):
        return 3


matrix = np.array([[convert_mat_element(e) for e in line.rstrip()]
                   for line in lines])
M, N = np.shape(matrix)
path_matrix = np.full((M, N), -1)


def is_in_matrix(point):
    return 0 <= point.x < M and 0 <= point.y < N


def was_reached(point):
    return is_in_matrix(point) and path_matrix[point.x, point.y] > -1


def set_path_index(point, index):
    path_matrix[point.x, point.y] = index


def get_path_index(point):
    return path_matrix[point.x, point.y]


def is_valid(point):
    return matrix[point.x, point.y] == 1


def set_free(point):
    matrix[point.x, point.y] = 1


def find_cheat_index_part1(point, step):
    cheat_pt = Point(point.x + 2*step[0], point.y + 2*step[1])
    if was_reached(cheat_pt):
        duration = get_path_index(point) - get_path_index(cheat_pt) - 2
        return (duration >= save_duration_thres)
    return False


def find_cheat_index_part2(point, path):
    nb_cheats = 0
    pt_index = get_path_index(point)
    max_index = max(0, pt_index-save_duration_thres-1)
    for path_index, path_pt in enumerate(path[0:max_index]):
        man_dist = point.man_dist(path_pt)
        duration = pt_index - path_index - man_dist
        if ((man_dist <= max_cheat_distance)
                and (duration >= save_duration_thres)):
            nb_cheats += 1
    return nb_cheats


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "(% s, % s)" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.x, self.y))

    def man_dist(self, other):
        return abs(other.x-self.x) + abs(other.y-self.y)

    def get_neighbors(self, path):
        nb_cheats_part1 = 0
        nb_cheats_part2 = 0
        valid_point = None

        for step in directions:
            new_pt = Point(self.x + step[0], self.y + step[1])
            if is_valid(new_pt) and not was_reached(new_pt):
                valid_point = new_pt
                continue
            if not is_valid(new_pt):
                nb_cheats_part1 += find_cheat_index_part1(self, step)
        nb_cheats_part2 += find_cheat_index_part2(self, path)
        return valid_point, nb_cheats_part1, nb_cheats_part2


# Part1
start_x, start_y = np.where(matrix == 2)
start_pt = Point(start_x[0], start_y[0])
set_free(start_pt)

path_matrix[start_x, start_y] = 0
path = [start_pt]

end_x, end_y = np.where(matrix == 3)
end_pt = Point(end_x[0], end_y[0])
set_free(end_pt)

pt = start_pt
path_index = 0
nb_cheats_part1 = 0
nb_cheats_part2 = 0

while pt != end_pt:
    path_index += 1
    new_pt, nb_saves_part1, nb_saves_part2 = pt.get_neighbors(path)
    nb_cheats_part1 += nb_saves_part1
    nb_cheats_part2 += nb_saves_part2
    pt = new_pt
    set_path_index(pt, path_index)
    path.append(pt)

_, _, nb_saves_part2 = end_pt.get_neighbors(path)

print("Part1", nb_cheats_part1)
print("Part2", nb_cheats_part2 + nb_saves_part2)

if plot:
    plt.figure()
    plt.imshow(matrix, cmap='gray')
    plt.figure()
    plt.imshow(path_matrix, cmap='gray')
