
elves = set()

with open("input.txt") as f:
    for r, line in enumerate(f.readlines()):
        line = line.strip()
        for col, c in enumerate(line):
            if c == "#":
                elves.add((r, col))


# def print_field(rows):
#     for row in rows:
#         print("".join(row))

def is_elf(elves, pos, offset):
    r = pos[0]+offset[0]
    c = pos[1]+offset[1]

    return (r, c) in elves


def choose_move(round, elves, pos):
    N_is_elf = is_elf(elves, pos, (-1, 0))
    NE_is_elf = is_elf(elves, pos, (-1, 1))
    NW_is_elf = is_elf(elves, pos, (-1, -1))

    S_is_elf = is_elf(elves, pos, (1, 0))
    SE_is_elf = is_elf(elves, pos, (1, 1))
    SW_is_elf = is_elf(elves, pos, (1, -1))

    E_is_elf = is_elf(elves, pos, (0, 1))

    W_is_elf = is_elf(elves, pos, (0, -1))

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


def move_elf(elves, curr_pos, new_pos):
    elves.remove(curr_pos)
    elves.add(new_pos)


def do_round_fast(round, elves):
    proposals = {}

    for elf in elves:
        # print(round, r, c)
        proposal = choose_move(round, elves, elf)

        if proposal == None:
            continue

        if proposal not in proposals:
            proposals[proposal] = []

        proposals[proposal].append(elf)

    if len(proposals) == 0:
        return False

    for proposal, elf_positions in proposals.items():
        if len(elf_positions) == 1:
            move_elf(elves, elf_positions[0], proposal)

    # print_field(rows)

    return True



# print_field(rows)

for round in range(200000):
    print(round)
    if not do_round_fast(round, elves):
        print("ended at " + str(round+1))
        break
    # print()

min_r = 999999
max_r = 0

min_c = 999999
max_c = 0


for elf in elves:
    r = elf[0]
    c = elf[1]

    min_r = min(min_r, r)
    max_r = max(max_r, r)

    min_c = min(min_c, c)
    max_c = max(max_c, c)

print(min_r, min_c)
print(max_r, max_c)