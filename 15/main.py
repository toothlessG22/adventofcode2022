import re

# sensors
# beacons

sensors = []
beacons = set()
mans = []

elims = set()

# y1 = 10
y1 = 2_000_000

offset = 0

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        matches = re.findall("-?\d+",line)

        nums = [int(n) for n in matches]


        sensors.append((nums[0], nums[1]))
        beacons.add((nums[2], nums[3]))

        if nums[3] == y1:
            offset += 1

        mans.append(abs(nums[0]-nums[2]) + abs(nums[1]-nums[3]))

for i in range(len(sensors)):
    print("i:", i, "sensor:",sensors[i],"man:", mans[i])

    if abs(sensors[i][1] - y1) <= mans[i]:
        spread = mans[i] - abs(sensors[i][1] - y1)

        print("spread:", spread)
        print("e1", sensors[i][0] - spread, "e2", sensors[i][0] + spread)
        for j in range(spread + 1):

            elims.add(sensors[i][0] - j)
            elims.add(sensors[i][0] + j)

print(len(elims))

print(offset)

print(len(elims)-1)

# max_y = 20
max_y = 4_000_000

edges = set()

def is_valid(edge):
    for i in range(len(sensors)):
        if abs(sensors[i][0]-edge[0])+abs(sensors[i][1]-edge[1]) <= mans[i]:
            return False

    return True


for y in range(0, max_y):
    # print(y)

    narrows = []
    edges = []

    for i in range(len(sensors)):
        spread = mans[i] - abs(sensors[i][1] - y)
        if spread > 0:
            e1 = sensors[i][0] - spread
            e2 = sensors[i][0] + spread

            # print("sensor", sensors[i], "man", mans[i] ,"edges", (e1,e2),"spread", spread)
            if e1 > 0 and e1 < max_y and is_valid(((e1-1),y)):
                print(((e1-1), y))

            if e2 > 0 and e2 < max_y and is_valid(((e2+1),y)):
                print(((e2+1), y))

pass