
rows = []

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()
        rows.append([c for c in line])

def add_row_top(rows):
    rows.insert(0, ["." for _ in range(len(rows[0]))])

def add_row_bottom(rows):
    rows.append(["." for _ in range(len(rows[0]))])

def add_col_left(rows):
    for row in rows:
        row.insert(0, ".")

def add_col_right(rows):
    for row in rows:
        row.append(".")

def print_field(rows):
    for row in rows:
        print("".join(row))

def is_elf(rows, pos, offset):
    r = pos[0]+offset[0]
    c = pos[1]+offset[1]

    if r < 0 or r >= len(rows):
        return False
    if c < 0 or c >= len(rows[0]):
        return False

    return rows[r][c] == "#"

def choose_move(round, rows, pos):
    N_is_elf = is_elf(rows, pos, (-1, 0))
    NE_is_elf = is_elf(rows, pos, (-1, 1))
    NW_is_elf = is_elf(rows, pos, (-1, -1))

    S_is_elf = is_elf(rows, pos, (1, 0))
    SE_is_elf = is_elf(rows, pos, (1, 1))
    SW_is_elf = is_elf(rows, pos, (1, -1))

    E_is_elf = is_elf(rows, pos, (0, 1))

    W_is_elf = is_elf(rows, pos, (0, -1))

    r, c = pos

    if not any([N_is_elf, NE_is_elf, NW_is_elf, S_is_elf, SE_is_elf, SW_is_elf, E_is_elf, W_is_elf]):
        return None

    cycle_i = round % 4

    N_move = (r-1, c) if not N_is_elf and not NE_is_elf and not NW_is_elf else None
    S_move = (r+1, c) if not S_is_elf and not SE_is_elf and not SW_is_elf else None
    W_move = (r, c - 1) if not W_is_elf and not NW_is_elf and not SW_is_elf else None
    E_move = (r, c+1) if not E_is_elf and not NE_is_elf and not SE_is_elf else None

    if cycle_i == 0:
        moves = [N_move, S_move, W_move, E_move]
    elif cycle_i == 1:
        moves = [S_move, W_move, E_move, N_move]
    elif cycle_i == 2:
        moves = [W_move, E_move, N_move, S_move]
    elif cycle_i == 3:
        moves = [E_move, N_move, S_move, W_move]

    for move in moves:
        if move is not None:
            return move

    return None

def move_elf(rows, curr_pos, new_pos):
    rows[curr_pos[0]][curr_pos[1]] = "."
    rows[new_pos[0]][new_pos[1]] = "#"

def do_round(round, rows):
    add_row_top(rows)
    add_row_bottom(rows)
    add_col_left(rows)
    add_col_right(rows)



    proposals = {}

    for r in range(len(rows)):
        for c in range(len(rows[0])):
            if rows[r][c] == "#":
                print(round, r, c)
                proposal = choose_move(round, rows, (r, c))

                if proposal == None:
                    continue

                if proposal not in proposals:
                    proposals[proposal] = []

                proposals[proposal].append((r, c))

    for proposal, elf_positions in proposals.items():
        if len(elf_positions) == 1:
            move_elf(rows, elf_positions[0], proposal)

    print_field(rows)



print_field(rows)

for round in range(10):
    print(round)
    do_round(round, rows)
    print()

min_r = 999999
max_r = 0

min_c = 999999
max_c = 0


for r in range(len(rows)):
    for c in range(len(rows[0])):
        if rows[r][c] == "#":
            min_r = min(min_r, r)
            max_r = max(max_r, r)

            min_c = min(min_c, c)
            max_c = max(max_c, c)

print(min_r, min_c)
print(max_r, max_c)

count = 0

for r in range(min_r, max_r+1):
    for c in range(min_c, max_c+1):
        if rows[r][c] == ".":
            count += 1

print(count)