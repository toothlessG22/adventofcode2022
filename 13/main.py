from functools import cmp_to_key

pairs = []


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

def is_valid(left, right):
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            valid = is_valid(left[i], right[i])

            if valid == False:
                return False

            if valid == True:
                return True

        if len(left) == len(right):
            return None

        return len(left) <= len(right)

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None

        return left < right

    if isinstance(left, int):
        return is_valid([left], right)
    else:
        return is_valid(left, [right])

for i in range(0, len(lines), 3):
    p_1 =  eval(lines[i])
    p_2 = eval(lines[i+1])

    pairs.append((p_1, p_2))

i = 1
count = 0

for pair in pairs:
    p_1 = pair[0]
    p_2 = pair[1]

    print(p_1, p_2, is_valid(p_1, p_2), i)
    v = is_valid(p_1, p_2)

    if v is None:
        pass

    if v:
        count += i
    i += 1


print(count)

packets = [eval(line) for line in lines if line != ""]

packets.append([[2]])
packets.append([[6]])

print()
packets= sorted(packets, key=cmp_to_key(lambda x, y: -1 if is_valid(x,y) else 1))

i = 1

six = None
two = None

for p in packets:
    print(p)
    if p == [[2]]:
        two = i
    elif p == [[6]]:
        six = i
    i += 1

print(six*two)



pass