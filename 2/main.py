AX = 1 + 3
AY = 2 + 6
AZ = 3 + 0

BX = 1 + 0
BY = 2 + 3
BZ = 3 + 6

CX = 1 + 6
CY = 2 + 0
CZ = 3 + 3
#
# score = 0
#
# with open("input.txt") as f:
#     for line in f.readlines():
#         line = line.strip()
#         if line == "A X":
#             score += AX
#         elif line == "A Y":
#             score += AY
#         elif line == "A Z":
#             score += AZ
#         elif line == "B X":
#             score += BX
#         elif line == "B Y":
#             score += BY
#         elif line == "B Z":
#             score += BZ
#         elif line == "C X":
#             score += CX
#         elif line == "C Y":
#             score += CY
#         elif line == "C Z":
#             score += CZ
#         else:
#             print("BROKE")
#
# print(score)

def get_score(line):
    if line == "A X":
        return AX
    elif line == "A Y":
        return AY
    elif line == "A Z":
        return AZ
    elif line == "B X":
        return BX
    elif line == "B Y":
        return BY
    elif line == "B Z":
        return BZ
    elif line == "C X":
        return CX
    elif line == "C Y":
        return CY
    elif line == "C Z":
        return CZ

score = 0

tie = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}

lose = {
    "A": "Z",
    "B": "X",
    "C": "Y"
}

win = {
    "A": "Y",
    "B": "Z",
    "C": "X"
}

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        if line[2] == "Y":
            score += get_score(line[:2] + tie[line[0]])
        if line[2] == "X":
            score += get_score(line[:2] + lose[line[0]])
        if line[2] == "Z":
            score += get_score(line[:2] + win[line[0]])

print(score)