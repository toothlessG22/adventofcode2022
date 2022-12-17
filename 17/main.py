with open("input.txt") as f:
    jets = f.readline().strip()


def get_row(rock):
    return rock[0]


def get_col(rock):
    return rock[1]


def move_rocks(rocks, d_r, d_c):
    return [ (get_row(rock) + d_r, get_col(rock)+d_c) for rock in rocks]


def are_new_rocks_valid(current_rocks, new_rocks):

    for new_rock in new_rocks:
        if new_rock in current_rocks:
            return False

        if get_row(new_rock) < 0:
            return False

        if get_col(new_rock) < 0 or get_col(new_rock) > 6:
            return False

    return True

ROCK_TYPES = 5


def generate_new_falling_rocks(starting_height, rock_type):
    if rock_type == 0:
        return [
            (starting_height, 2),
            (starting_height, 3),
            (starting_height, 4),
            (starting_height, 5)
        ]
    elif rock_type == 1:
        return [
            (starting_height + 2, 3),

            (starting_height + 1, 2),
            (starting_height + 1, 3),
            (starting_height + 1, 4),

            (starting_height, 3),
        ]
    elif rock_type == 2:
        return [
            (starting_height + 2, 4),

            (starting_height + 1, 4),

            (starting_height, 2),
            (starting_height, 3),
            (starting_height, 4),
        ]
    elif rock_type == 3:
        return [
            (starting_height + 3, 2),
            (starting_height + 2, 2),
            (starting_height + 1, 2),
            (starting_height, 2),
        ]
    elif rock_type == 4:
        return [
            (starting_height + 1, 2),
            (starting_height + 1, 3),
            (starting_height, 2),
            (starting_height, 3),
        ]

    raise Exception("Bad rock type")

def print_rocks(falling_rocks, current_rocks):
    top_rock_height = 0
    for rock in falling_rocks:
        top_rock_height = max(top_rock_height, get_row(rock))
    for rock in current_rocks:
        top_rock_height = max(top_rock_height, get_row(rock))

    for r in range(top_rock_height,top_rock_height-20,-1):
        msg = ""

        for c in range(7):
            node = (r,c)
            if node in falling_rocks:
                msg += "@"
            elif node in current_rocks:
                msg += "#"
            else:
                msg += "."

        print(msg)

# this isn't needed, I overestimated how long it would take to form a loop
def prune_rocks(current_rocks, max_rocks_height):
    return set({rock for rock in current_rocks if max_rocks_height - get_row(rock) < 100})


# this is over complex, I overestimated how long it would take to form a loop
def top_90_rows_as_tuple(current_rocks, max_height):
    nums = []

    for i in range(10):
        num = 0
        offset = i * 9

        for j in range(9):
            bit_offset = j * 7

            for k in range(7):

                r = max_height - (offset + j)

                if (r, k) in current_rocks:
                    num |= (1 << (bit_offset + k))

        nums.append(num)

    return tuple(nums)


jet_i = 0

current_rocks = set()

p2_range = 1_000_000_000_000 % len(jets)

drops = {}

drop_tracing = set()

top_90_match = None

rock_i_heights = {}

for rock_i in range(100000):

    max_rocks_height = 0
    for rock in current_rocks:
        max_rocks_height = max(max_rocks_height, get_row(rock) + 1)

    rock_i_heights[rock_i] = max_rocks_height

    if rock_i % 1000 == 0:
        current_rocks = prune_rocks(current_rocks, max_rocks_height)

    falling_rocks = generate_new_falling_rocks(max_rocks_height + 3, rock_i % ROCK_TYPES)
    # print(jet_i)

    drop = (jet_i % len(jets), rock_i % ROCK_TYPES)
    # print(len(drops))
    if drop not in drops:
        drops[drop] = set()

    new_top_90 = top_90_rows_as_tuple(current_rocks, max_rocks_height)
    if rock_i == 467:
        print(jet_i % len(jets), rock_i % ROCK_TYPES, new_top_90)
        print_rocks(falling_rocks, current_rocks)

    # print(jet_i % len(jets), rock_i % ROCK_TYPES, new_top_90)
    # print_rocks(falling_rocks, current_rocks)

    drop_tracing.add((drop, new_top_90, rock_i))

    if new_top_90 in drops[drop]:
        top_90_match = new_top_90
        print(jet_i % len(jets), rock_i % ROCK_TYPES, new_top_90)
        print_rocks(falling_rocks, current_rocks)
        break
    else:
        drops[drop].add(new_top_90)


    while True:
        # print(jet_i)
        # print_rocks(falling_rocks, current_rocks)
        # print()
        # print()

        # apply jet
        d_c = 1 if jets[jet_i % len(jets)] == ">" else -1
        jet_i += 1

        jet_moved_rocks = move_rocks(falling_rocks, 0, d_c)
        if are_new_rocks_valid(current_rocks, jet_moved_rocks):
            falling_rocks = jet_moved_rocks

        gravity_moved_rocks = move_rocks(falling_rocks, -1, 0)
        if are_new_rocks_valid(current_rocks, gravity_moved_rocks):
            falling_rocks = gravity_moved_rocks
        else:

            current_rocks.update(falling_rocks)
            # print("locked")
            # print_rocks(falling_rocks, current_rocks)
            # print()
            # print()
            break

max_rocks_height = 0
for rock in current_rocks:
    max_rocks_height = max(max_rocks_height, get_row(rock))

loop_i_s = []

for drop_trace in drop_tracing:
    if drop_trace[1] == top_90_match:
        loop_i_s.append(drop_trace[2])


print(loop_i_s)
print(rock_i_heights[loop_i_s[0]], rock_i_heights[loop_i_s[1]])

start_i = loop_i_s[0]
start_height = rock_i_heights[loop_i_s[0]]

delta_rocks = loop_i_s[1] - loop_i_s[0]
delta_height = rock_i_heights[loop_i_s[1]] - rock_i_heights[loop_i_s[0]]

delta_mult = (1_000_000_000_000 - start_i) // delta_rocks

remaining_offset = 1_000_000_000_000 - start_i - (delta_rocks * delta_mult)

print(start_height + (delta_mult * delta_height) + (rock_i_heights[loop_i_s[0]+remaining_offset]-rock_i_heights[loop_i_s[0]]))