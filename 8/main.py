height = []



with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()
        height.append([int(c) for c in line])

width = len(height)
height_num = len(height[0])

visible = [[False for _ in range(len(height[0]))] for _ in range(len(height))]

# TOP
# LEFT
# RIGHT
# BOTTOM

for x in range(height_num):
    min_for_visible = -1
    for y in range(0, width):
        if height[x][y] > min_for_visible:
            min_for_visible = height[x][y]
            visible[x][y] = True

    min_for_visible = -1
    for y in range(width-1, -1, -1):
        if height[x][y] > min_for_visible:
            min_for_visible = height[x][y]
            visible[x][y] = True

for y in range(width):
    min_for_visible = -1
    for x in range(0, height_num):
        if height[x][y] > min_for_visible:
            min_for_visible = height[x][y]
            visible[x][y] = True

    min_for_visible = -1
    for x in range(height_num-1, -1, -1):
        if height[x][y] > min_for_visible:
            min_for_visible = height[x][y]
            visible[x][y] = True

count = 0

for x in range(height_num):
    for y in range(width):
        if visible[x][y]:
            count += 1

print(count)
print(visible)

max_score = 0

for x in range(height_num):
    for y in range(width):
        score = 1
        cur_height = height[x][y]

        print(x,y, cur_height)

        sub_score = 0
        for y_1 in range(y+1, width):
            sub_score += 1
            print(x, y_1, height[x][y_1])
            if height[x][y_1] >= cur_height:
                break
        score *= sub_score

        print(sub_score)

        sub_score = 0
        for y_1 in range(y-1, -1, -1):
            sub_score += 1
            if height[x][y_1] >= cur_height:
                break

        score *= sub_score

        print(sub_score)

        sub_score = 0
        for x_1 in range(x-1, -1, -1):
            sub_score += 1
            if height[x_1][y] >= cur_height:
                break

        score *= sub_score

        print(sub_score)

        sub_score = 0
        for x_1 in range(x+1, height_num):
            sub_score += 1
            if height[x_1][y] >= cur_height:
                break

        score *= sub_score

        print(sub_score)

        max_score = max(max_score, score)

print(max_score)
