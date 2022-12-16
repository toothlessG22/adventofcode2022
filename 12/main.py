
current_pos = ()
target_pos = ()

map = []

with open("input.txt") as f:
    for r, line in enumerate(f.readlines()):
        line = line.strip()

        map.append([])

        for col, c in enumerate(line):

            if c == "S":
                current_pos = (r, col)
                c = "z"
            elif c == "E":
                target_pos = (r, col)
                c = "z"

            map[-1].append(c)

q = [current_pos]
visited = set(q)
parents = {}

rows = len(map)
columns = len(map[0])

def try_get_child(r, c, map):

    if r < 0 or r >= rows or c < 0 or c >= columns:
        return None, "z"

    return (r, c), map[r][c]

def get_children(r, c, map):
    curr_height = ord(map[r][c])

    possible_children = [
        try_get_child(r + 1, c, map),
        try_get_child(r - 1, c, map),
        try_get_child(r, c + 1, map),
        try_get_child(r, c - 1, map),
    ]

    children = []

    for (possible_child_height) in possible_children:
        if possible_child_height[0] is not None and ord(possible_child_height[1])-curr_height <= 1:
            children.append(possible_child_height[0])

    return children


while len(q) > 0:
    curr = q.pop(0)

    if curr == target_pos:
        break

    for child in get_children(curr[0], curr[1], map):
        if child not in visited:
            visited.add(child)
            parents[child] = curr
            q.append(child)

curr = target_pos
count = 0

while curr != current_pos:
    curr = parents[curr]
    count += 1

print(count)
pass