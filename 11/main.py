
operand1s = []
ops = []
operand2s = []
tests = []
trues = []
falses = []
worry_levels = []

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        if line.startswith("Starting items: "):
            data = line.split(": ")[-1]
            starting_items = [int(item) for item in data.split(", ")]
            worry_levels.append(starting_items)

        elif line.startswith("Operation: "):
            operand1 = line.split(" ")[-3]
            op = line.split(" ")[-2]
            operand2 = line.split(" ")[-1]

            operand1s.append(operand1)
            ops.append(op)
            operand2s.append(operand2)
        elif line.startswith("Test: "):
            num = int(line.split(" ")[-1])
            tests.append(num)
        elif line.startswith("If true: "):
            trues.append(int(line.split(" ")[-1]))
        elif line.startswith("If false: "):
            falses.append(int(line.split(" ")[-1]))

monkey_inspection_counts = [0 for i in range(len(worry_levels))]

mod_val = 1

for test in tests:
    mod_val *= test

for round_i in range(10000):
    print(round_i)
    for monkey_i in range(len(worry_levels)):
        for worrylevel in worry_levels[monkey_i]:
            new_worry_level = 0

            monkey_inspection_counts[monkey_i] += 1

            if ops[monkey_i] == "*":
                if operand2s[monkey_i] == "old":
                    new_worry_level = worrylevel * worrylevel
                else:
                    new_worry_level = worrylevel * int(operand2s[monkey_i])
            else:
                if operand2s[monkey_i] == "old":
                    new_worry_level = worrylevel + worrylevel
                else:
                    new_worry_level = worrylevel + int(operand2s[monkey_i])

            new_worry_level = new_worry_level % mod_val

            test = False
            if new_worry_level % tests[monkey_i] == 0:
                test = True

            if test:
                worry_levels[trues[monkey_i]].append(new_worry_level)
            else:
                worry_levels[falses[monkey_i]].append(new_worry_level)

        worry_levels[monkey_i] = []


print(monkey_inspection_counts)
