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

class Block:
    def __init__(self, size):
        self.size = size
        self.position = None
        
    def set_position_and_compute_score(self, position, file):
        self.position = position
        return compute_score(position, file, self.size)
    
blocks_map = dict([(int(index/2), Block(e)) for index, e in enumerate(line) if (index % 2) == 0])
position = 0

for index, size in enumerate(line):
    if (index % 2) == 0:
        file = index / 2
        if not blocks_map[file].position:
            res_part2 += blocks_map[file].set_position_and_compute_score(position, file)
        position += blocks_map[file].size
    else:
        while size > 0:
            try:
                file, block = next((f, b) for (f, b) in list(blocks_map.items())[::-1] if (not b.position and b.size <= size))
                res_part2 += blocks_map[file].set_position_and_compute_score(position, file)
                position += block.size
                size -= block.size
            except StopIteration:
                position += size
                break
        
print("Part2:", res_part2)
