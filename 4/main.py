
count = 0

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        ranges = line.split(",")

        range_1 = [int(s) for s in ranges[0].split("-")]
        range_2 = [int(s) for s in ranges[1].split("-")]

        range_1_nums = [x for x in range(range_1[0], range_1[1] + 1)]

        for i in range(range_2[0], range_2[1]+1):
            if i in range_1_nums:
                count += 1
                break

print(count)