
dir_children = {}
file_children = {}

dirs = set()
dir_stack = []

file_sizes = {}

current_dir = "/"


with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if line[:4] == "$ cd":
            current_dir = line[5:]

            if current_dir == "..":
                dir_stack.pop()
                current_dir = dir_stack[-1]
            elif current_dir == "/":
                dir_stack = ["/"]
            else:
                dir_stack.append(current_dir)

            current_dir = "/".join(dir_stack)

            if current_dir not in dirs:
                dir_children[current_dir] = []
                file_children[current_dir] = []
                dirs.add(current_dir)

        elif line[:4] == "$ ls":
            pass
        elif line[:3] == "dir":
            dir_name = line[4:]
            dir_children[current_dir].append(current_dir + "/" + dir_name)
        else:
            size, name = line.split(" ")
            size = int(size)

            file_sizes[current_dir + "/" + name] = size
            file_children[current_dir].append(current_dir + "/" + name)

dir_sizes = {}
dirs_left = list(dirs)

def can_calc_size(dir, dir_sizes, dir_children):
    for dir_child in dir_children[dir]:
        if dir_child not in dir_sizes:
            return False

    return True

def calc_size(dir, dir_size, dir_children, file_children, file_sizes):
    size = 0

    for dir_child in dir_children[dir]:
        size += dir_size[dir_child]

    for file_child in file_children[dir]:
        size += file_sizes[file_child]

    return  size

while len(dirs_left) > 0:
    print(dir_sizes)
    for dir in dirs_left:
        print(dir, dir_children[dir])
        if can_calc_size(dir, dir_sizes, dir_children):
            dir_sizes[dir] = calc_size(dir, dir_sizes, dir_children, file_children, file_sizes)
            dirs_left.remove(dir)

total = 0

for v in dir_sizes.values():
    if v <= 100000:
        total += v

print(dir_sizes)

needed_space = dir_sizes["/"] - 40000000

min_total = 99999999999

for v in dir_sizes.values():
    if v >= needed_space:
        min_total = min(min_total, v)

print(min_total)
pass
