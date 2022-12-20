import math

file = []

with open("input.txt") as f:
    for line in f.readlines():
        num = int(line)

        file.append(num)

if len(set(file)) < len(file):
    raise Exception()

original_file = file[:]

mod = (len(original_file)-1)


def swap(file, s1, s2):
    if s1 == 1 and s2 == 0:
        file = file[1:] + [file[0]]

    if s1 == fil

    tmp = file[s1]
    file[s1] = file[s2]
    file[s2] = tmp


def index_helper(current_index, moves):
    if moves > 0:

for to_mix in original_file:
    current_index = file.index(to_mix)

    if to_mix > 0:
        offset = to_mix // len(file) * len(file)
    else:
        offset = math.ceil(to_mix / len(file)) * len(file)

    num_swaps = to_mix - offset

    print(current_index, num_swaps)

    if num_swaps == 0:
        continue
    elif num_swaps < 0:
        for i in range(0, num_swaps, -1):
            print("swap", current_index+i, current_index+i-1)
            swap(file, current_index+i, current_index+i-1)
            print(file)
    else:
        for i in range(0, num_swaps):
            print("swap", current_index + i, current_index + i + 1)
            swap(file, current_index + i, current_index + i + 1)

    print(file)

pass

