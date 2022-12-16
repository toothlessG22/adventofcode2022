X = 1

xs = [1]

cycle = 0

total = 0

crt = [["." for _ in range(40)] for _ in range(6)]


def add_to_total(cycle, total, x):
    if (cycle % 40) - 20 == 0:
        return total + (cycle-1 * x)
    return total


def get_pixel_coords(cycle):
    base_coords = cycle % 240
    return (base_coords // 40, base_coords % 40)


def should_light_pixel(cycle, x):
    if abs(cycle%40-x) > 1:
        return False
    return True


def run_cycle(cycle, crt, x, addx):
    print(f"Running Cycle {cycle}")
    print(f"CRT Drawing {get_pixel_coords(cycle)} {should_light_pixel(cycle, x)}")
    print(f"X Val {x}")

    coords =  get_pixel_coords(cycle)
    if should_light_pixel(cycle,x):
        crt[coords[0]][coords[1]] = "#"
    else:
        crt[coords[0]][coords[1]] = "."

    return (cycle+1, x + addx)

x = 1

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        s_line = line.split(" ")

        if s_line[0] == "noop":
            cycle, x = run_cycle(cycle, crt, x, 0)
            # cycle +=1
            # xs.append(xs[-1])
            #
            # total = add_to_total(cycle, total, xs[-1])
            # coords = get_pixel_coords(cycle)
            # if should_light_pixel(cycle, xs[-1]):
            #     crt[coords[0]][coords[1]] = "#"
            # else:
            #     crt[coords[0]][coords[1]] = "."


        elif s_line[0] == "addx":
            cycle, x = run_cycle(cycle, crt, x, 0)
            cycle, x = run_cycle(cycle, crt, x, int(s_line[1]))
            # cycle += 1
            # xs.append(xs[-1])
            # total = add_to_total(cycle, total, xs[-1])
            # coords = get_pixel_coords(cycle)
            # if should_light_pixel(cycle, xs[-1]):
            #     crt[coords[0]][coords[1]] = "#"
            # else:
            #     crt[coords[0]][coords[1]] = "."
            #
            # cycle += 1
            # xs.append(xs[-1] + int(s_line[1]))
            # total = add_to_total(cycle, total, xs[-1])
            # coords = get_pixel_coords(cycle)
            # if should_light_pixel(cycle, xs[-1]):
            #     crt[coords[0]][coords[1]] = "#"
            # else:
            #     crt[coords[0]][coords[1]] = "."

print(total)

for x in crt:
    print("".join(x))
