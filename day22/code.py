#!/usr/bin/env python
from collections import deque
from types import SimpleNamespace

file = 'input'

f = open(file, 'r')
lines = list(f)
nb_steps = 2000

numbers = [int(e) for e in lines]

modulo_factor = int(2**24)


def compute(nb):
    nb = (nb * 64 ^ nb) % modulo_factor
    nb = (int(nb / 32) ^ nb) % modulo_factor
    return (2048 * nb ^ nb) % modulo_factor


prices = {}
res_part1 = 0

for nb_index, nb in enumerate(numbers):
    diffs = deque()
    last_digit = nb % 10

    for i in range(0, nb_steps):
        nb = compute(nb)
        diffs.append(nb % 10 - last_digit)
        last_digit = nb % 10

        if (len(diffs) == 5):
            diffs.popleft()
            sequence = tuple(diffs)
            if sequence not in prices:
                prices[sequence] = SimpleNamespace(total_price=last_digit,
                                                   last_buyer=nb_index)
            else:
                if prices[sequence].last_buyer != nb_index:
                    prices[sequence].last_buyer = nb_index
                    prices[sequence].total_price += last_digit
    res_part1 += nb

res_part2 = max(prices.values(), key=lambda e: e.total_price).total_price

print("Part1:", res_part1)
print("Part2:", res_part2)
