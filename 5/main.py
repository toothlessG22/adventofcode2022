import re


stacks = [[] for _ in range(1000)]

with open("input.txt") as f:
    line = f.readline()[:-1]

    while line != "" and line[1] != "1":

        for i in range(1, len(line), 4):
            if line[i] != " ":
                stack_i = i // 4
                stacks[stack_i].append(line[i])

        line = f.readline()[:-1]

    f.readline()
    instructions = f.readlines()

for stack in stacks:
    stack.reverse()

for instruction in instructions:
    nums = re.findall(r"\d+", instruction)

    amount = int(nums[0])
    start = int(nums[1])-1
    end = int(nums[2])-1

    tmp = stacks[start][-amount:]
    stacks[start] = stacks[start][:-amount]
    stacks[end] += tmp
    pass

msg = ""

for stack in stacks:
    if len(stack) > 0:
        msg += stack[-1]

print(msg)

pass