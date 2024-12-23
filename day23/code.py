#!/usr/bin/env python
import rustworkx as rx
from rustworkx.visualization import mpl_draw
from itertools import combinations

file = 'input'
plot = False
f = open(file, 'r')
lines = list(f)

graph = rx.PyGraph(multigraph=False)
lan_to_node_index_map = dict()

for line in lines:
    lhs, rhs = line.rstrip().split("-")
    if lhs not in lan_to_node_index_map:
        lhs_index = graph.add_node(lhs)
        lan_to_node_index_map[lhs] = lhs_index
    else:
        lhs_index = lan_to_node_index_map[lhs]
    if rhs not in lan_to_node_index_map:
        rhs_index = graph.add_node(rhs)
        lan_to_node_index_map[rhs] = rhs_index
    else:
        rhs_index = lan_to_node_index_map[rhs]
    graph.add_edge(lhs_index, rhs_index, [])


def get_hash(index1, index2, index3):
    sorted_list = sorted([index1, index2, index3])
    return hash(tuple(sorted_list))


found_cycles = set()

for lan, node_index in lan_to_node_index_map.items():
    if lan[0] != 't':
        continue
    adjacent_nodes = graph.adj(node_index).keys()
    for pair in combinations(adjacent_nodes, 2):
        if graph.has_edge(pair[0], pair[1]):
            cycle_hash = get_hash(node_index, pair[0], pair[1])
            if cycle_hash not in found_cycles:
                found_cycles.add(cycle_hash)


print("Part1", len(found_cycles))


solutions = []


def BronKerbosch(max_clique, P, X):
    if len(P) == 0 and len(X) == 0:
        solutions.append(max_clique)
        return
    while len(P) > 0:
        node = P.pop()
        node_neighbors = set(graph.adj(node).keys())
        BronKerbosch(max_clique.union({node}),
                     P.union({node}).intersection(node_neighbors),
                     X.intersection(node_neighbors))
        X.add(node)


BronKerbosch(set(), set(graph.node_indices()), set())

max_solution = max(solutions, key=lambda e: len(e))
code = sorted([graph[node] for node in max_solution])

res_part2 = ''
for e in code:
    res_part2 += e+','

print("Part2", res_part2[:-1])

if plot:
    mpl_draw(graph, alpha=0.5, with_labels=True)
