#!/usr/bin/env python
import numpy as np

file = 'input'

f = open(file, 'r')
lines_input = list(f)

wall_val = 0
left_box_val = 1
right_box_val = 2
free_val = 3
init_pos_val = 4


def convert_mat_element(e):
    if (e == '.'):
        return free_val
    if (e == 'O'):
        return left_box_val
    if (e == '#'):
        return wall_val
    if (e == '@'):
        return init_pos_val


def convert_mat_element_part2(e):
    if (e == '.'):
        return [free_val, free_val]
    if (e == 'O'):
        return [left_box_val, right_box_val]
    if (e == '#'):
        return [wall_val, wall_val]
    if (e == '@'):
        return [init_pos_val, free_val]


def convert_line_part2(line):
    res = []
    for e in line.rstrip():
        res.extend(convert_mat_element_part2(e))
    return res


def convert_travel_element(e):
    if (e == '^'):
        return 0
    if (e == '>'):
        return 1
    if (e == 'v'):
        return 2
    if (e == '<'):
        return 3


def go_north(point):
    return Point(point.x-1, point.y)


def go_east(point):
    return Point(point.x, point.y+1)


def go_south(point):
    return Point(point.x+1, point.y)


def go_west(point):
    return Point(point.x, point.y-1)


directions_map = {
    0: go_north,
    1: go_east,
    2: go_south,
    3: go_west
}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "(% s, % s)" % (self.x, self.y)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.x, self.y))

    def get_element(self):
        return matrix[self.x, self.y]


class Box:
    def __init__(self, pt, element=None):
        if not element:
            element = pt.get_element()
        if (element == left_box_val):
            self.left_pt = pt
            self.right_pt = go_east(pt)
        else:
            self.right_pt = pt
            self.left_pt = go_west(pt)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.left_pt == other.left_pt
                and self.right_pt == other.right_pt)

    def __hash__(self):
        return hash((self.left_pt, self.right_pt))

    def __repr__(self):
        return "[% s, % s]" % (self.left_pt, self.right_pt)

    def __str__(self):
        return self.__repr__()

    def move(self, direction):
        return Box(directions_map[direction](self.left_pt), left_box_val)

    def meet_wall(self, direction):
        if direction % 2 == 0:
            moved = self.move(direction)
            return is_wall(moved.left_pt) or is_wall(moved.right_pt)
        elif (direction == 1):
            return is_wall(go_east(self.right_pt))
        else:
            return is_wall(go_west(self.left_pt))

    def get_adjacent_boxes(self, direction):
        moved = self.move(direction)

        if direction % 2 == 0:
            boxes = []
            if is_box(moved.left_pt):
                boxes.append(Box(moved.left_pt))
            if is_box(moved.right_pt):
                boxes.append(Box(moved.right_pt))
            return boxes

        elif (direction == 1):
            if is_box(moved.right_pt):
                return [Box(moved.right_pt)]
        else:
            if is_box(moved.left_pt):
                return [Box(moved.left_pt)]

        return []


def set_free(point):
    matrix[point.x, point.y] = free_val


def set_box(point):
    matrix[point.x, point.y] = left_box_val


def set_box_part2(box):
    matrix[box.left_pt.x, box.left_pt.y] = left_box_val
    matrix[box.right_pt.x, box.right_pt.y] = right_box_val


def set_free_part2(box):
    matrix[box.left_pt.x, box.left_pt.y] = free_val
    matrix[box.right_pt.x, box.right_pt.y] = free_val


def is_wall(point):
    return (matrix[point.x, point.y] == wall_val)


def is_box(point):
    return (matrix[point.x, point.y] in [left_box_val, right_box_val])


def is_free(point):
    return (matrix[point.x, point.y] == free_val)


def push_box(init_pt, direction):
    pt = init_pt
    while is_box(pt):
        pt = directions_map[direction](pt)

    if is_wall(pt):
        return False

    set_free(init_pt)
    set_box(pt)
    return True


def all_can_move(boxes, direction):
    list_boxes = []

    for box in boxes:
        if box.meet_wall(direction):
            return False, []

        adj_boxes = box.get_adjacent_boxes(direction)
        if len(adj_boxes) == 0:
            continue
        res, new_boxes = all_can_move(adj_boxes, direction)
        if not res:
            return False, []
        list_boxes.extend(new_boxes)

    list_boxes.extend(boxes)
    return True, list_boxes


def move_all(boxes, direction):
    for box in boxes:
        new_box = box.move(direction)
        set_box_part2(new_box)
        set_free_part2(box)


def push_box_part2(init_pt, direction):
    boxes = []
    pt = init_pt
    while is_box(pt):
        boxes.append(Box(pt))
        pt = directions_map[direction](pt)
        if (direction % 2 == 1):
            pt = directions_map[direction](pt)

    if is_wall(pt):
        return False

    if direction % 2 == 1:
        for box in boxes:
            set_box_part2(box.move(direction))

    else:
        can_move, to_move_boxes = all_can_move([boxes[0]], direction)
        if not can_move:
            return False
        to_move_boxes = list(dict.fromkeys(to_move_boxes))
        move_all(to_move_boxes, direction)

    set_free(init_pt)
    return True


def compute_next_point(point, direction, part2):
    new_pt = directions_map[direction](point)
    if is_wall(new_pt):
        return point
    if is_free(new_pt):
        return new_pt
    if (not part2):
        succ = push_box(new_pt, direction)
    else:
        succ = push_box_part2(new_pt, direction)
    if succ:
        return new_pt
    return point


def compute_result():
    boxes = np.where(matrix == left_box_val)
    positions = list(zip(*boxes))
    return sum([100 * x + y for x, y in positions])


separator = lines_input.index("\n")
travel = [convert_travel_element(
    e) for line in lines_input[separator+1:] for e in line.rstrip()]

# Part1
matrix = np.array([[convert_mat_element(e) for e in line.rstrip()]
                  for line in lines_input[0:separator]])
x, y = np.where(matrix == init_pos_val)
point = Point(x[0], y[0])
set_free(point)
part2 = False

for direction in travel:
    point = compute_next_point(point, direction, part2)

print("Part1", compute_result())

# Part2
matrix = np.array([convert_line_part2(line)
                  for line in lines_input[0:separator]])
x, y = np.where(matrix == init_pos_val)
point = Point(x[0], y[0])
set_free(point)
part2 = True

for i, direction in enumerate(travel):
    point = compute_next_point(point, direction, part2)

print("Part2", compute_result())
