#!/usr/bin/env python

file = 'input'
           
f = open(file,'r')
line = [int(e) for e in list(f)[0].rstrip()]
N = len(line)

def compute_score(position, file, size):
    return file*(size*position+size*(size-1)/2)

res_part1 = 0

reverse_index = N-1
reverse_size = line[reverse_index]

file = 0
reverse_file = int((N-1)/2)

position = 0

for index, size in enumerate(line):
    if (index % 2) == 0:
        if (file == reverse_file):
            size = reverse_size
        res_part1 += compute_score(position, file, size)
        position += size
        file += 1
    else:
        count = 0
        while(count < size):
            res_part1 += position * reverse_file
            position += 1
            count += 1
            reverse_size -= 1
            if reverse_size == 0:
                reverse_file -= 1
                reverse_index -= 2
                reverse_size = line[reverse_index]
    if (file > reverse_file):
        break

print("Part1:", res_part1)

        
res_part2 = 0

block_sizes = [e for index, e in enumerate(line) if (index % 2) == 0]
max_file = int((N-1)/2)
                 
def find_first_valid_blocks(size, block_moved_indexes):
    res = []
    while size > 0:
        found_sol = False
        for index, e in enumerate(block_sizes[::-1]):
            if (index in block_moved_indexes):
                continue
            if (e <= size):
                res.append([e, max_file-index])
                block_moved_indexes.add(index)
                size -= e
                found_sol = True
                break
        if (not found_sol):
            break
    return res, size

block_moved_indexes = set()
cur_position = 0
cur_file = 0

for index, number in enumerate(line):
    if (index % 2) == 0:
        block_reverse_index = int((N-index) / 2)
        if block_reverse_index in block_moved_indexes:
            cur_file += 1
            cur_position += block_sizes[int(index/2)]
            continue
        for j in range(number):
            res_part2 += cur_position * cur_file
            cur_position += 1
        cur_file += 1
    else:
        sizes, remaining = find_first_valid_blocks(number, block_moved_indexes)
        for size, file in sizes:
            for j in range(size):
                res_part2 += cur_position * file
                cur_position += 1
        cur_position += remaining
    
        
print("Part2:", res_part2)

#10923582871568 too high