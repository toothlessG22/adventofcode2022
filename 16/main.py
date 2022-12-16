
tunnels = {}
flows ={}
names = []

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        line = line.replace(",","")
        s_line_semi = line.split(";")

        flow = int(s_line_semi[0].split("=")[1])

        s_line_space = line.split(" ")

        name = s_line_space[1]

        valve_tunnels = []

        i = -1
        while s_line_space[i] != "valves" and s_line_space[i] != "valve":
            valve_tunnels.append(s_line_space[i])
            i -= 1

        tunnels[name] = valve_tunnels
        flows[name] = flow
        names.append(name)

time_map = {}



def get_opening_value(time_at_open, flow):
    return time_at_open * flow


p = {}

def get_best_time_to_reach_nodes(tunnels, current_pos):
    global p

    q = [current_pos]
    visited = set(q)
    dist = {}
    dist[current_pos] = 0
    p[current_pos] = None

    while len(q) > 0:
        v = q.pop(0)
        for tunnel in tunnels[v]:
            if tunnel not in visited:
                visited.add(tunnel)
                dist[tunnel] = dist[v] + 1
                p[tunnel] = v
                q.append(tunnel)

    return dist

get_best_time_to_reach_nodes(tunnels, "AA")

for n1 in names:
    time_map[n1] = {}
    best_times = get_best_time_to_reach_nodes(tunnels, n1)
    for n2 in best_times:
        time_map[n1][n2] = best_times[n2]

opened = {"DD"}
time = 30

opening_val_map = {i:{name:get_opening_value(i,flows[name]) for name in names} for i in range(31)}

names_to_check = list(filter(lambda x: flows[x] != 0, sorted(names, key=lambda x: opening_val_map[30][x], reverse=True)))

# for name in names:
#     if name not in opened:
#         print(name, get_opening_value(time-best_time_to_reach_nodes[name]-1, flows[name]), time-best_time_to_reach_nodes[name])

best_score = 0
best_path = ""

calls = 0


# def back_track(available, time_left, curr_pos, total_score, path):
#     if time_left <= 0:
#         return
#
#     global best_score
#     global best_path
#
#     global calls
#     calls += 1
#
#     if calls % 1000000 == 0:
#         print(calls)
#         print(best_score)
#
#     # print(available, time_left, curr_pos, total_score)
#     if total_score > best_score:
#         best_score = total_score
#         best_path = path
#
#     if len(available) == 0:
#         return
#
#     # go somewhere else and open
#     for name in name_test_orders:
#         if name not in available or name == curr_pos:
#             continue
#
#         if time_left == 30:
#             print(time_left, name, best_score, time_map[curr_pos][name])
#
#         time_of_open = time_left - time_map[curr_pos][name] - 1
#
#         if time_of_open > 0:
#             available.remove(name)
#             back_track(available, time_of_open, name, total_score + opening_val_map[time_of_open][name], path + f"-{name} open @ {time_of_open}*{flows[name]}={opening_val_map[time_of_open][name]}-")
#             available.add(name)

# def back_track(available, time_left, curr_pos, total_score, path):
#     global best_score
#     global best_path
#
#     global calls
#     calls += 1
#
#     if calls % 1000000 == 0:
#         print(calls)
#         print(best_score)
#
#     # print(available, time_left, curr_pos, total_score)
#     path += "-" + curr_pos
#     best_score = max(best_score, total_score)
#     if time_left == 0 or len(available) == 0:
#         best_score = max(best_score, total_score)
#         best_path = path
#         print(best_score)
#         return
#
#     if total_score + sum([opening_val_map[time_left][name] for name in available]) < best_score:
#         return
#
#     # open current
#     if curr_pos in available:
#         available.remove(curr_pos)
#         back_track(available, time_left-1, curr_pos, total_score + opening_val_map[time_left-1][curr_pos], path + "-open" + curr_pos + "[" + str(flows[curr_pos]) + "](" + str(opening_val_map[time_left-1][curr_pos]) +")@" + str(time_left-1))
#         available.add(curr_pos)
#
#     # go somewhere else
#     for name in name_test_orders:
#         if name not in available or name == curr_pos:
#             continue
#         if time_left == 30:
#             print(time_left, name, best_score, time_map[curr_pos][name])
#         time_to_move = time_map[curr_pos][name]
#         if time_to_move < time_left:
#             back_track(available, time_left - time_to_move, name, total_score, path)

def back_track(available, p_time_at_open, e_time_at_open, p_target, e_target, total_score,): #path):
    if p_time_at_open <= 0 or e_time_at_open <= 0:
        return

    if p_time_at_open >= e_time_at_open:
        time_at_open = p_time_at_open
        target = p_target
        e = False
    else:
        time_at_open = e_time_at_open
        target = e_target
        e = True

    global best_score
    global best_path
    global calls
    calls += 1

    if calls % 1000000 == 0:
        print(calls)
        print(best_score)

    if total_score > best_score:
        best_score = total_score
        # best_path = path

    best_possible_score = 0
    for name in available:
        p_dist = time_map[p_target][name]
        e_dist = time_map[e_target][name]

        p_arrival = p_time_at_open - p_dist - 1
        e_arrival = e_time_at_open - e_dist - 1

        if p_arrival <= 0 and e_arrival <= 0:
            continue

        if p_arrival > e_arrival:
            best_possible_score += opening_val_map[p_arrival][name]
        else:
            best_possible_score += opening_val_map[e_arrival][name]

    if total_score + best_possible_score < best_score:
        return

    if len(available) == 0:
        return

    # go somewhere else and open
    for name in names_to_check:
        if name not in available or name == target:
            continue

        if p_time_at_open == 26:
            print(p_time_at_open, name, best_score, time_map[target][name])

        new_time_at_open = time_at_open - time_map[target][name] - 1

        if new_time_at_open > 0:
            available.remove(name)
            back_track(available,
                       p_time_at_open if e else new_time_at_open,
                       new_time_at_open if e else e_time_at_open,
                       p_target if e else name,
                       name if e else e_target,
                       total_score + opening_val_map[new_time_at_open][name],)
                       # path + f"-{'elephant' if e else 'person'} open {name} @ {26-new_time_at_open} for {opening_val_map[new_time_at_open][name]}-")
            available.add(name)


back_track(set(names_to_check), 26, 26, "AA", "AA", 0)

print(best_score)
print(best_path)

pass