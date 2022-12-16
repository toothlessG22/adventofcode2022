
elfs = []

current = 0

with open("input1.txt") as f:
    for line in f:
        if line.strip() == "":
            elfs.append(current)
            current = 0
        else:
            current += int(line.strip())

elfs.append(current)

print(sum(sorted(elfs,reverse=True)[:3]))