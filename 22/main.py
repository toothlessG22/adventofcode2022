import re
from enum import Enum

rows = []

cols = 0

directions = ""

with open("input.txt") as f:
    for line in f.readlines():
        if line.strip() == "":
            continue

        if line[0].isdigit():
            directions = line
            continue

        line = line[:-1]
        line = line.replace(" ", "T")
        cols = max(cols, len(line))
        rows.append(line)



for r in range(len(rows)):
    rows[r] = ["T"] + [c for c in rows[r].ljust(cols, "T")] + ["T"]

cols = cols + 2

rows.insert(0, ["T" for _ in range(cols)])
rows.append(["T" for _ in range(cols)])

current_pos = None


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def get_direction_character(direction: Direction):
    if direction == Direction.UP:
        return "^"
    elif direction == Direction.DOWN:
        return "v"
    elif direction == Direction.LEFT:
        return "<"
    elif direction == Direction.RIGHT:
        return ">"


def get_direction_update(direction: Direction):
    if direction == Direction.UP:
        return (-1, 0)
    elif direction == Direction.DOWN:
        return (1, 0)
    elif direction == Direction.LEFT:
        return (0, -1)
    elif direction == Direction.RIGHT:
        return (0, 1)

def get_new_dir(direction_update, current_direction: Direction):
    if direction_update == "R":
        if current_direction == Direction.UP:
            return Direction.RIGHT
        elif current_direction == Direction.DOWN:
            return Direction.LEFT
        elif current_direction == Direction.LEFT:
            return Direction.UP
        elif current_direction == Direction.RIGHT:
            return Direction.DOWN
    else:
        if current_direction == Direction.UP:
            return Direction.LEFT
        elif current_direction == Direction.DOWN:
            return Direction.RIGHT
        elif current_direction == Direction.LEFT:
            return Direction.DOWN
        elif current_direction == Direction.RIGHT:
            return Direction.UP

def print_board(rows, current_pos, current_dir):
    tmp = rows[current_pos[0]][current_pos[1]]
    rows[current_pos[0]][current_pos[1]] = get_direction_character(current_dir)

    for r in range(len(rows)):
        print("".join(rows[r]))

    rows[current_pos[0]][current_pos[1]] = tmp

current_dir = Direction.RIGHT

for c, tile in enumerate(rows[1]):
    if tile == ".":
        current_pos = (1, c)
        break

tmp_current_pos = tuple(current_pos)
tmp_current_dir = current_dir


# print_board(rows, current_pos, current_dir)

directions = [int(d) if d[0].isdigit() else d for d in list(re.findall(r"(\d+|L|R)", directions))]


def apply_update(rows, pos, update):
    row_count = len(rows)
    col_count = len(rows[0])

    return ((pos[0] + update[0]) % row_count, (pos[1] + update[1]) % col_count)

def get_tile(rows, pos):
    return rows[pos[0]][pos[1]]

for direction in directions:

    if isinstance(direction, int):
        update = get_direction_update(current_dir)

        for _ in range(direction):
            possible_new_pos = apply_update(rows, current_pos, update)
            tile = get_tile(rows, possible_new_pos)

            while tile == "T":
                possible_new_pos = apply_update(rows, possible_new_pos, update)
                tile = get_tile(rows, possible_new_pos)

            if tile == "#":
                break

            current_pos = possible_new_pos
    else:
        current_dir = get_new_dir(direction, current_dir)

    # print_board(rows, current_pos, current_dir)
    # print()

print(current_pos, current_dir)

def get_direction_score(direction: Direction):
    if direction == Direction.UP:
        return 3
    elif direction == Direction.DOWN:
        return 1
    elif direction == Direction.LEFT:
        return 2
    elif direction == Direction.RIGHT:
        return 0

print(1000 * current_pos[0] + 4 * current_pos[1] + get_direction_score(current_dir))


CUBE_WIDTH = 50 # 4

horixedges = {

}

# def generate_t_map_entries(cube_width, p1_start, p2_start, p1_horiz, p2_horiz, p1_entry_dir, p1_exit_dir, p2_entry_dir, p2_exit_dir, p1_row_off, p1_col_off, p2_row_off, p2_col_off, reverse):
#
#     p1_curr = (p1_start[0] * cube_width + 1 + p1_row_off, p1_start[1] * cube_width + 1 + p1_col_off)
#     p2_curr = (p2_start[0] * cube_width + 1 + p2_row_off, p2_start[1] * cube_width + 1 + p2_col_off)
#
#     p1_offset = (0, 1) if p1_horiz else (1, 0)
#     p2_offset = (0, 1) if p2_horiz else (1, 0)
#
#     p1_entries = []
#     p2_entries = []
#
#     for _ in range(cube_width):
#         p1_entries.append(p1_curr)
#         p2_entries.append(p2_curr)
#
#         p1_curr = (p1_curr[0] + p1_offset[0], p1_curr[1] + p1_offset[1])
#         p2_curr = (p2_curr[0] + p2_offset[0], p2_curr[1] + p2_offset[1])
#
#     if reverse:
#         p2_entries.reverse()
#
#     for i in range(len(p1_entries)):
#         p1_curr = p1_entries[i]
#         p2_curr = p2_entries[i]
#
#         t_map[(p1_curr, p1_entry_dir)] = (p2_curr, p1_exit_dir)
#         t_map[(p2_curr, p2_entry_dir)] = (p1_curr, p2_exit_dir)

current_pos = tmp_current_pos
current_dir = tmp_current_dir

def get_entry_dir_offset(cube_width, direction):
    if direction == Direction.UP:
        return (-1, 0)
    elif direction == Direction.DOWN:
        return (-1, 0)
    elif direction == Direction.LEFT:
        return (0, -1)
    elif direction == Direction.RIGHT:
        return (0, cube_width)

def get_exit_dir_offset(cube_width, direction):
    if direction == Direction.UP:
        return (-1, 0)
    elif direction == Direction.DOWN:
        return (cube_width, 0)
    elif direction == Direction.LEFT:
        return (0, -1)
    elif direction == Direction.RIGHT:
        return (0, cube_width)

def tp(cube_width, current_position, entry_coord, entry_dir, exit_coord, exit_dir):
    reverse_offset = cube_width - 1

    exit_dir_offset = get_exit_dir_offset(cube_width, exit_dir)

    base_entry_coord = (entry_coord[0] * cube_width + 1, entry_coord[1] * cube_width + 1)
    rel_coords = (current_position[0] - base_entry_coord[0], current_position[1] - base_entry_coord[1])

    base_new_coord = (exit_coord[0] * cube_width + 1 + exit_dir_offset[0], exit_coord[1] * cube_width + 1 + exit_dir_offset[1])

    if entry_dir == Direction.LEFT:
        rel_coord = rel_coords[0]

        if exit_dir == Direction.LEFT:
            return (base_new_coord[0] + rel_coord, base_new_coord[1])
        elif exit_dir == Direction.UP:
            return (base_new_coord[0], base_new_coord[1] + reverse_offset - rel_coord)
        elif exit_dir == Direction.DOWN:
            return (base_new_coord[0], base_new_coord[1] + rel_coord)
        elif exit_dir == Direction.RIGHT:
            return (base_new_coord[0] + reverse_offset - rel_coord, base_new_coord[1])

    if entry_dir == Direction.RIGHT:
        rel_coord = rel_coords[0]

        if exit_dir == Direction.RIGHT:
            return (base_new_coord[0] + rel_coord, base_new_coord[1])
        elif exit_dir == Direction.UP:
            return (base_new_coord[0], base_new_coord[1] + rel_coord)
        elif exit_dir == Direction.DOWN:
            return (base_new_coord[0], base_new_coord[1] + reverse_offset -  rel_coord)
        elif exit_dir == Direction.LEFT:
            return (base_new_coord[0] + reverse_offset - rel_coord, base_new_coord[1])

    if entry_dir == Direction.UP:
        rel_coord = rel_coords[1]

        if exit_dir == Direction.UP:
            return (base_new_coord[0], base_new_coord[1] + rel_coord)
        elif exit_dir == Direction.LEFT:
            return (base_new_coord[0] + reverse_offset - rel_coord, base_new_coord[1])
        elif exit_dir == Direction.RIGHT:
            return (base_new_coord[0] + rel_coord, base_new_coord[1])
        elif exit_dir == Direction.DOWN:
            return (base_new_coord[0], base_new_coord[1] + reverse_offset - rel_coord)

    if entry_dir == Direction.DOWN:
        rel_coord = rel_coords[1]

        if exit_dir == Direction.DOWN:
            return (base_new_coord[0], base_new_coord[1] + rel_coord)
        elif exit_dir == Direction.LEFT:
            return (base_new_coord[0] + rel_coord, base_new_coord[1])
        elif exit_dir == Direction.RIGHT:
            return (base_new_coord[0] + reverse_offset - rel_coord, base_new_coord[1])
        elif exit_dir == Direction.UP:
            return (base_new_coord[0], base_new_coord[1] + reverse_offset - rel_coord)


# t_map = {
#     ((-1, 2), Direction.UP): ((0, 0), Direction.DOWN),
#     ((0, 0), Direction.UP): ((-1, 2), Direction.DOWN),
#
#     ((0, 1), Direction.LEFT): ((0, 1), Direction.DOWN),
#     ((0, 1), Direction.UP): ((0, 1), Direction.RIGHT),
#
#     ((0, 3), Direction.RIGHT): ((2, 4), Direction.LEFT),
#     ((2, 4), Direction.RIGHT): ((0, 3), Direction.LEFT),
#
#     ((1, -1), Direction.LEFT): ((3, 3), Direction.UP),
#     ((3, 3), Direction.DOWN): ((1, -1), Direction.UP),
#
#     ((1, 3), Direction.RIGHT): ((1, 3), Direction.DOWN),
#     ((1, 3), Direction.UP): ((1, 3), Direction.LEFT),
#
#     ((2, 1), Direction.DOWN): ((2, 1), Direction.RIGHT),
#     ((2, 1), Direction.UP): ((2, 1), Direction.LEFT),
#
#     ((2, 0), Direction.DOWN): ((3, 2), Direction.UP),
#     ((3, 2), Direction.DOWN): ((2, 0), Direction.UP),
# }

t_map = {
    ((1, 2), Direction.DOWN): ((1, 2), Direction.LEFT),
    ((1, 2), Direction.RIGHT): ((1, 2), Direction.UP),

    ((1, 0), Direction.UP): ((1, 0), Direction.RIGHT),
    ((1, 0), Direction.LEFT): ((1, 0), Direction.DOWN),

    ((3, 1), Direction.RIGHT): ((3, 1), Direction.UP),
    ((3, 1), Direction.DOWN): ((3, 1), Direction.LEFT),

    ((0, 3), Direction.RIGHT): ((2, 2), Direction.LEFT),
    ((2, 2), Direction.RIGHT): ((0, 3), Direction.LEFT),

    ((-1, 2), Direction.UP): ((4, 0), Direction.UP),
    ((4, 0), Direction.DOWN): ((-1, 2), Direction.DOWN),

    ((-1, 1), Direction.UP): ((3, -1), Direction.RIGHT),
    ((3, -1), Direction.LEFT): ((-1, 1), Direction.DOWN),

    ((0, 0), Direction.LEFT): ((2, -1), Direction.RIGHT),
    ((2, -1), Direction.LEFT): ((0, 0), Direction.RIGHT),
}

for direction in directions:

    print_board(rows, current_pos, current_dir)

    if isinstance(direction, int):
        for _ in range(direction):
            update = get_direction_update(current_dir)
            possible_new_pos = apply_update(rows, current_pos, update)
            possible_new_dir = current_dir
            tile = get_tile(rows, possible_new_pos)

            if tile == "T":
                entry_coord = (possible_new_pos[0]-1) // CUBE_WIDTH, (possible_new_pos[1]-1) // CUBE_WIDTH
                search = (entry_coord, current_dir)

                if entry_coord == (-1, 1):
                    x = 2
                    pass

                if search not in t_map:
                    assert False

                exit_coord, exit_dir = t_map[search]

                possible_new_pos = tp(CUBE_WIDTH, possible_new_pos, entry_coord, current_dir, exit_coord, exit_dir)
                possible_new_dir = exit_dir

                tile = get_tile(rows, possible_new_pos)

                print("after tp")
                print_board(rows, possible_new_pos, possible_new_dir)
                print()

                if tile == "T":
                    assert False

            if tile == "#":
                break

            current_pos = possible_new_pos
            current_dir = possible_new_dir

            print("after pos change")
            print_board(rows, current_pos, current_dir)
            print()
    else:
        current_dir = get_new_dir(direction, current_dir)

        print("after dir change")
        print_board(rows, current_pos, current_dir)
        print()


print(current_pos, current_dir)
print(1000 * current_pos[0] + 4 * current_pos[1] + get_direction_score(current_dir))