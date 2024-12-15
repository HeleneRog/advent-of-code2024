#!/usr/bin/env python
import copy
import rustworkx as rx
from typing import NamedTuple

file = 'input'

f = open(file, 'r')
init_pebbles = [int(e) for e in list(f)[0].rstrip().split(" ")]


def evolve(pebble):
    if (pebble == 0):
        return [1]
    pebble_str = str(pebble)
    str_size = len(pebble_str)
    if (str_size % 2 == 0):
        return [int(pebble_str[:str_size//2]), int(pebble_str[str_size//2:])]
    else:
        return [pebble * 2024]


def one_step(pebbles):
    new_pebbles = list()
    for pebble in pebbles:
        new_pebbles.extend(evolve(pebble))
    return new_pebbles


# Part1
pebbles = copy.copy(init_pebbles)
for i in range(0, 25):
    pebbles = one_step(pebbles)
print("Part1", len(pebbles))


# Part2
nb_steps = 75

graph = rx.PyDiGraph(check_cycle=False)
pebble_to_node_index_map = dict()


class Pebble(NamedTuple):
    index: int
    sizes: dict


def compute(node, nb_steps):
    if (nb_steps == 0):
        return 1
    if nb_steps in graph[node].sizes:
        return graph[node].sizes[nb_steps]

    children_nodes = list(graph.successor_indices(node))
    if len(children_nodes) == 0:
        new_pebbles = evolve(graph[node].index)
        for pebble in new_pebbles:
            if pebble in pebble_to_node_index_map:
                child_node = pebble_to_node_index_map[pebble]
                graph.add_edge(node, child_node, None)
            else:
                child_node = graph.add_child(node, Pebble(pebble, {}), None)
                pebble_to_node_index_map[pebble] = child_node
            children_nodes.append(child_node)
    graph[node].sizes[nb_steps] = sum(
        [compute(e, nb_steps-1) for e in children_nodes])
    return graph[node].sizes[nb_steps]


res_part2 = 0
for pebble in init_pebbles:
    if pebble not in pebble_to_node_index_map:
        index = graph.add_node(Pebble(pebble, {}))
        pebble_to_node_index_map[pebble] = index
    res_part2 += compute(pebble_to_node_index_map[pebble], nb_steps)

print("Part2:", res_part2)
