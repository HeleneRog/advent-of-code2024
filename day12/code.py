#!/usr/bin/env python
import numpy as np
from scipy.ndimage import label, find_objects
import copy

file = 'input'

f = open(file, 'r')
lines = list(f)

mat = np.array([[ord(e) for e in line.rstrip()]
               for line in lines], dtype=np.uint32)
values = np.sort(np.unique(mat))
directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]


def is_in_mat(i, j, matrice):
    M, N = np.shape(matrice)
    return 0 <= i < M and 0 <= j < N


def compute_perimeter(mat, points, zone_label):
    perimeter = 0
    for pt in points:
        for di, dj in directions:
            i, j = [pt[0] + di, pt[1] + dj]
            if not is_in_mat(i, j, mat) or mat[i, j] != zone_label:
                perimeter += 1
    return perimeter


def compute_sides_number(mat, points, zone_label):
    neighboors = [dict() for i in range(0, len(directions))]

    for pt in points:
        for index, (di, dj) in enumerate(directions):
            i, j = [pt[0] + di, pt[1] + dj]
            if not is_in_mat(i, j, mat) or mat[i, j] != zone_label:
                if (di == 0):
                    i, j = j, i
                if i not in neighboors[index]:
                    neighboors[index][i] = []
                neighboors[index][i].append(j)

    nb_elements = 0
    for neighboor in neighboors:
        for pts in neighboor.values():
            diff = np.diff(sorted(pts))
            nb_elements += np.size(np.where(diff > 1)) + 1
    return nb_elements


def solve(mat, values, func):
    res = 0
    for value in values:
        slices = find_objects(mat, value)

        for aslice in slices:
            if aslice:
                submat = copy.copy(mat[aslice])
                submat[submat != value] = 0
                labelled, nb_labels = label(submat)

                for zone_label in range(1, nb_labels+1):
                    positions = list(zip(*np.where(labelled == zone_label)))
                    res += len(positions) * \
                        func(labelled, positions, zone_label)
        mat[mat == value] = values[-1] + 1
    return res


print("Part1", solve(copy.copy(mat), values, compute_perimeter))
print("Part2", solve(copy.copy(mat), values, compute_sides_number))
