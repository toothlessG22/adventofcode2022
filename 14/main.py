used_spots = set()

highest_point = 0

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()
        points = []
        for point in line.split(" -> "):
            s_point = point.split(",")
            points.append((int(s_point[0]), int(s_point[1])))
            highest_point = max(highest_point,points[-1][1])

        for i in range(1, len(points)):
            p1 = points[i-1]
            p2 = points[i]

            if p1[0] == p2[0]:
                for j in range(min(p1[1], p2[1]),max(p1[1], p2[1])+1):
                    used_spots.add((p1[0], j))

            elif p1[1] == p2[1]:
                for j in range(min(p1[0], p2[0]),max(p1[0], p2[0])+1):
                    used_spots.add((j, p1[1]))

for i in range(0, 1001):
    used_spots.add((i, highest_point+2))

count = 0

not_done = True

while (500, 0) not in used_spots:
    curr_sand_pos = (500, 0)
    at_rest = False
    count += 1
    print(count)

    while True:
        # print(curr_sand_pos)

        if (curr_sand_pos[0], curr_sand_pos[1]+1) not in used_spots:
            curr_sand_pos = (curr_sand_pos[0], curr_sand_pos[1]+1)
        elif (curr_sand_pos[0]-1, curr_sand_pos[1]+1) not in used_spots:
            curr_sand_pos = (curr_sand_pos[0]-1, curr_sand_pos[1]+1)
        elif (curr_sand_pos[0]+1, curr_sand_pos[1]+1) not in used_spots:
            curr_sand_pos = (curr_sand_pos[0]+1, curr_sand_pos[1]+1)
        else:
            used_spots.add(curr_sand_pos)
            at_rest = True
            break

    if not at_rest:
        break

print(count)

pass