cubes = set()

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        cubes.add(eval(f"({line})"))


def sides_exposed(cubes, test_cube):
    count = 0

    if (test_cube[0]+1, test_cube[1], test_cube[2]) not in cubes:
        count += 1
    if (test_cube[0]-1, test_cube[1], test_cube[2]) not in cubes:
        count += 1
    if (test_cube[0], test_cube[1]+1, test_cube[2]) not in cubes:
        count += 1
    if (test_cube[0], test_cube[1]-1, test_cube[2]) not in cubes:
        count += 1
    if (test_cube[0], test_cube[1], test_cube[2]+1) not in cubes:
        count += 1
    if (test_cube[0], test_cube[1], test_cube[2]-1) not in cubes:
        count += 1

    return count

total = 0

for cube in cubes:
    total += sides_exposed(cubes, cube)

print(total)


def get_neighbors(cubes, test_cube):
    neighbors = []

    if (test_cube[0] + 1, test_cube[1], test_cube[2]) not in cubes:
        neighbors.append((test_cube[0] + 1, test_cube[1], test_cube[2]))

    if (test_cube[0] - 1, test_cube[1], test_cube[2]) not in cubes:
        neighbors.append((test_cube[0] - 1, test_cube[1], test_cube[2]))

    if (test_cube[0], test_cube[1]+1, test_cube[2]) not in cubes:
        neighbors.append((test_cube[0], test_cube[1]+1, test_cube[2]))

    if (test_cube[0], test_cube[1]-1, test_cube[2]) not in cubes:
        neighbors.append((test_cube[0], test_cube[1]-1, test_cube[2]))

    if (test_cube[0], test_cube[1], test_cube[2]+1) not in cubes:
        neighbors.append((test_cube[0] + 1, test_cube[1], test_cube[2]+1))

    if (test_cube[0], test_cube[1], test_cube[2]-1) not in cubes:
        neighbors.append((test_cube[0] + 1, test_cube[1], test_cube[2]-1))

    return neighbors

def can_bfs_out(cube, cubes_out, cubes_not_out):
    q = [cube]
    visited = set(q)

    while len(q) != 0:
        node = q.pop(0)
        if node == (-1,-1,-1) or node in cubes_out:
            return True

        if node in cubes_not_out:
            return False

        for neighbor in get_neighbors(cubes, node):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)

    return False

cubes_to_add = set()

cubes_out = set()

for i in range(20):

    for j in range(20):
        for k in range(20):
            print(i, j, k)
            if not can_bfs_out((i, j, k), cubes_out, cubes_to_add):
                cubes_to_add.add((i, j, k))
            else:
                cubes_out.add((i, j, k))

total_2 = 0

cubes = cubes.union(cubes_to_add)

for cube in cubes:
    total_2 += sides_exposed(cubes, cube)

print(total_2)