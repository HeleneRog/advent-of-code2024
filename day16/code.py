#!/usr/bin/env python
import numpy as np
import rustworkx as rx
from rustworkx.visualization import mpl_draw
import matplotlib.pyplot as plt
from math import inf

file = 'input'
plot = False
f = open(file, 'r')
lines_input = list(f)
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
                  for line in lines_input])


def is_wall(point):
    return (matrix[point.x, point.y] == 0)


def is_free(point):
    return (matrix[point.x, point.y] == 1)


def set_free(point):
    matrix[point.x, point.y] = 1


class Point:
    def __init__(self, point):
        self.x = point.x
        self.y = point.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "(% s, % s)" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()


class PointDirection:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def is_same_position(self, other):
        return (isinstance(other, self.__class__)
                and self.x == other.x and self.y == other.y)

    def __eq__(self, other):
        return (self.is_same_position(other)
                and self.direction % 2 == other.direction % 2)

    def __repr__(self):
        return "(% s, % s, % s)" % (self.x, self.y, self.direction)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.x, self.y, self.direction % 2))

    def turn_right(self):
        turn_right = (self.direction + 1) % 4
        step = directions[turn_right]
        return PointDirection(self.x + step[0], self.y + step[1], turn_right)

    def turn_left(self):
        turn_left = (self.direction - 1) % 4
        step = directions[turn_left]
        return PointDirection(self.x + step[0], self.y + step[1], turn_left)

    def go_straight(self):
        step = directions[self.direction]
        return PointDirection(self.x + step[0], self.y + step[1],
                              self.direction)


def compute_neighbors(point):
    points = []

    straight = point.go_straight()
    if is_free(straight):
        points.append([straight, 0])

    right = point.turn_right()
    if is_free(right):
        points.append([right, 1000])

    left = point.turn_left()
    if is_free(left):
        points.append([left, 1000])

    return points


graph = rx.PyGraph(multigraph=False)


def build_graph(pt, prev_node_index):
    cost = 1
    neighbors = compute_neighbors(pt)
    edges_points = []

    while len(neighbors) == 1:
        edges_points.append(Point(pt))
        cost += neighbors[0][1] + 1
        pt = neighbors[0][0]
        if pt.is_same_position(end_pos):
            break
        neighbors = compute_neighbors(pt)

    if pt in map_pt_to_index:
        node_index = map_pt_to_index[pt]
        graph.add_edge(prev_node_index, node_index, [cost, edges_points])
    else:
        node_index = graph.add_node(pt)
        map_pt_to_index[pt] = node_index
        graph.add_edge(prev_node_index, node_index, [cost, edges_points])

        ortho_pt = PointDirection(pt.x, pt.y, (pt.direction + 1) % 2)
        ortho_node_index = graph.add_node(ortho_pt)
        map_pt_to_index[ortho_pt] = ortho_node_index
        graph.add_edge(node_index, ortho_node_index, [1000, []])

        for neighbor_pt, cost in neighbors:
            if (cost == 0):
                build_graph(neighbor_pt, node_index)
            else:
                build_graph(neighbor_pt, ortho_node_index)


# Part1
init_x, init_y = np.where(matrix == 2)
init_pos = PointDirection(init_x[0], init_y[0], 1)
set_free(init_pos)

start_index = graph.add_node(init_pos)
map_pt_to_index = {init_pos: start_index}

end_x, end_y = np.where(matrix == 3)
for i in range(0, 2):
    end_pos = PointDirection(end_x[0], end_y[0], i)
    end_index = graph.add_node(end_pos)
    map_pt_to_index[end_pos] = end_index

set_free(end_pos)


init_neighbors = compute_neighbors(init_pos)

for neighbor_pt, cost in init_neighbors:
    new_pt = PointDirection(init_pos.x, init_pos.y, neighbor_pt.direction)
    if new_pt not in map_pt_to_index:
        node_index = graph.add_node(new_pt)
        map_pt_to_index[new_pt] = node_index
    else:
        node_index = map_pt_to_index[new_pt]
    graph.add_edge(start_index, node_index, [cost, []])
    build_graph(neighbor_pt, node_index)


res_part1 = inf
end_node_index_solution = 0
for i in range(0, 2):
    end_pos = PointDirection(end_x[0], end_y[0], i)
    sols = rx.dijkstra_shortest_path_lengths(
        graph, start_index, lambda edge: edge[0], map_pt_to_index[end_pos])
    for index, sol in sols.items():
        if sol < res_part1:
            res_part1 = sol
            end_node_index_solution = index

print("Part1", int(res_part1))

# Part2
sols = rx.graph_all_shortest_paths(
    graph, start_index, target=end_node_index_solution,
    weight_fn=lambda edge: edge[0])

points_set = set()
points_set.add(Point(graph[end_node_index_solution]))
for sol in sols:
    for previous, current in zip(sol, sol[1:]):
        point = graph[previous]
        points_set.add(Point(point))
        edges_pts = graph.get_edge_data(previous, current)[1]
        points_set.update(edges_pts)

res_part2 = len(points_set)
print("Part2", res_part2)


def print_position(point):
    step = directions[point.direction]
    return [10*(point.y + 0.5*step[1]), 10*(-point.x - 0.5*step[0])]


if plot:
    for pt in points_set:
        matrix[pt.x, pt.y] = 4
    plt.figure()
    plt.imshow(matrix, cmap='gray')

    inv_map = {index: print_position(pt)
               for pt, index in map_pt_to_index.items()}
    mpl_draw(graph, with_labels=True, edge_labels=lambda edge: edge[0],
             font_size=4, node_size=100, pos=inv_map)
