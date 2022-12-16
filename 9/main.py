#R
#C

rope = [(0,0) for _ in range(10)]
head = (0, 0)
tail = (0, 0)

tail_visited = set()

def reconcile_knot(head_pos, tail_pos):

    row_diff = head_pos[0] - tail_pos[0]
    abs_row_diff = abs(row_diff)
    col_diff = head_pos[1] - tail_pos[1]
    abs_col_diff = abs(col_diff)

    # tail in same spot or tail within 1
    if abs_row_diff <= 1 and abs_col_diff <= 1:
        return tail_pos

    # tail in same row (move 1 towards head)
    if abs_row_diff == 0:
        return (tail_pos[0], (tail_pos[1]+ head_pos[1])//2)

    # tail in same col ()
    if abs_col_diff == 0:
        return ((tail_pos[0] + head_pos[0]) // 2, tail_pos[1])


    if abs_row_diff == 2 and abs_col_diff == 2:
        return ((tail_pos[0] + head_pos[0]) // 2, (tail_pos[1] + head_pos[1]) // 2)

    if row_diff < 0 and col_diff < 0:
        return (tail_pos[0]-1, tail_pos[1]-1)

    if row_diff > 0 and col_diff < 0:
        return (tail_pos[0]+1, tail_pos[1]-1)

    if row_diff < 0 and col_diff > 0:
        return (tail_pos[0]-1, tail_pos[1]+1)

    if row_diff > 0 and col_diff > 0:
        return (tail_pos[0]+1, tail_pos[1]+1)


    pass

def return_new_head_pos(head_pos, single_command):
    new_head_pos = None

    if single_command == "R":
        new_head_pos = (head_pos[0], head_pos[1]+1)
    elif single_command == "L":
        new_head_pos = (head_pos[0], head_pos[1]-1)
    elif single_command == "U":
        new_head_pos = (head_pos[0]+1, head_pos[1])
    elif single_command == "D":
        new_head_pos = (head_pos[0]-1, head_pos[1])

    return new_head_pos

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        split_line = line.split(" ")

        command = split_line[0]
        s_count = split_line[1]

        count = int(s_count)

        for _ in range(count):
            print(rope)
            rope[0] = return_new_head_pos(rope[0], command)
            for i in range(1, 10):
                rope[i] = reconcile_knot(rope[i-1], rope[i])
            tail_visited.add(rope[9])

print(len(tail_visited))