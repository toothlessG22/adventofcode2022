
def lower_to_prio(c):
    return ord(c) - 96

def upper_to_prio(c):
    return ord(c) - 64 + 26

total = 0

# with open("input.txt") as f:
#     for rucksack in f.readlines():
#         h = int(len(rucksack)/2)
#
#         first = rucksack[:h]
#         second = rucksack[h:]
#
#         for s_c in second:
#             if s_c in first:
#                 if s_c.isupper():
#                     total += upper_to_prio(s_c)
#                 else:
#                     total += lower_to_prio(s_c)
#                 break

with open("input.txt") as f:
    lines = list(f.readlines())

    for i in range(0, len(lines), 3):
        available_c1 = lines[i]

        available_c2 = []
        for c in lines[i+1]:
            if c in available_c1:
                available_c2.append(c)

        available_c3 = []
        for c in lines[i+2]:
            if c in available_c2:
                available_c3.append(c)

        s_c = available_c3[0]
        if s_c.isupper():
            total += upper_to_prio(s_c)
        else:
            total += lower_to_prio(s_c)


print(total)