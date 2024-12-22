#!/usr/bin/env python
file = 'input'

f = open(file, 'r')
lines = list(f)
depth1 = 2
depth2 = 25

transitions_dir = {}

transitions_dir['AA'] = ['']
transitions_dir['A^'] = ['<']
transitions_dir['A<'] = ['v<<']
transitions_dir['Av'] = ['<v', 'v<']
transitions_dir['A>'] = ['v']

transitions_dir['^^'] = ['']
transitions_dir['^A'] = ['>']
transitions_dir['^<'] = ['v<']
transitions_dir['^v'] = ['v']
transitions_dir['^>'] = ['v>', '>v']

transitions_dir['<<'] = ['']
transitions_dir['<A'] = ['>>^']
transitions_dir['<^'] = ['>^']
transitions_dir['<v'] = ['>']
transitions_dir['<>'] = ['>>']

transitions_dir['vv'] = ['']
transitions_dir['vA'] = ['>^', '^>']
transitions_dir['v^'] = ['^']
transitions_dir['v<'] = ['<']
transitions_dir['v>'] = ['>']

transitions_dir['>>'] = ['']
transitions_dir['>A'] = ['^']
transitions_dir['>^'] = ['^<', '<^']
transitions_dir['><'] = ['<<']
transitions_dir['>v'] = ['<']


def compute_position(carac):
    if carac == '0':
        return [1, 0]
    if carac == 'A':
        return [2, 0]
    k = int(carac)
    return [(k-1) % 3, (k-1)//3 + 1]


def find_possible_sequences(e1, e2):
    pt1 = compute_position(e1)
    pt2 = compute_position(e2)
    dx = pt2[0]-pt1[0]
    dy = pt2[1]-pt1[1]
    dx_str = ''
    if (dx > 0):
        dx_str = '>'*dx
    if (dx < 0):
        dx_str = '<'*abs(dx)
    dy_str = ''
    if (dy > 0):
        dy_str = '^'*dy
    if (dy < 0):
        dy_str = 'v'*abs(dy)

    if (e1 in ['A', '0'] and e2 in ['1', '4', '7']):
        return [dy_str+dx_str+'A']

    if (e2 in ['A', '0'] and e1 in ['1', '4', '7']):
        return [dx_str+dy_str+'A']
    return [dx_str+dy_str+'A', dy_str+dx_str+'A']


sequences_size = {}


def compute_len(sequence, depth):
    key = str(depth)+sequence

    if (depth == 0):
        sequences_size[key] = len(sequence)
        return len(sequence)

    if key in sequences_size:
        return sequences_size[key]

    size = 0
    for e1, e2 in zip('A'+sequence, sequence):
        size += min([compute_len(transition+'A', depth-1)
                    for transition in transitions_dir[e1+e2]])
    sequences_size[key] = size
    return size


transitions_numeric_size = {}

res_part1 = 0
res_part2 = 0

for line in lines:
    line = line.rstrip()
    total_size_part1 = 0
    total_size_part2 = 0

    for e1, e2 in zip('A'+line, line):
        if e1+e2 not in transitions_numeric_size:
            sequences = find_possible_sequences(e1, e2)
            len1 = min([compute_len(seq, depth1) for seq in sequences])
            len2 = min([compute_len(seq, depth2) for seq in sequences])
            transitions_numeric_size[e1+e2] = [len1, len2]

        total_size_part1 += transitions_numeric_size[e1+e2][0]
        total_size_part2 += transitions_numeric_size[e1+e2][1]

    res_part1 += total_size_part1 * int(line[0:3])
    res_part2 += total_size_part2 * int(line[0:3])


print("Part1:", res_part1)
print("Part2:", res_part2)
