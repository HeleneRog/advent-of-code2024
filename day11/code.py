#!/usr/bin/env python

file_results = 'example'

f = open(file_results,'r')
pebbles = [int(e) for e in list(f)[0].rstrip().split(" ")]


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
for i in range(0, 25):
    pebbles = one_step(pebbles)
print("Part1", len(pebbles))

