

with open("input.txt") as f:
    buffer = f.readline()

for i in range(14, len(buffer)):
    if len(set(buffer[i-14:i])) == 14:
        print(i)
        break
