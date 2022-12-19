import re
from enum import Enum
from functools import lru_cache
import math
import time

blueprints = []

blueprint = []

def get_ore_robot_cost(blueprint):
    return blueprint[0]

def get_clay_robot_cost(blueprint):
    return blueprint[1]

def get_obsidian_robot_cost(blueprint):
    return blueprint[2]

def get_geode_robot_cost(blueprint):
    return blueprint[3]


with open("input.txt") as f:
    for i, line in enumerate(f.readlines()):
        line = line.strip()

        nums = [int(n) for n in re.findall("\d+", line)]

        blueprints.append((nums[1], nums[2] , (nums[3], nums[4]), (nums[5], nums[6])))

if len(blueprint) > 0:
    blueprints.append(blueprint)

pass


def get_build_choices(blueprint, obsidian, clay, ore):
    choices = []

    # geode
    geo_ore_cost, geo_obs_cost = get_geode_robot_cost(blueprint)
    if ore >= geo_ore_cost and obsidian >= geo_obs_cost:
        choices.append(((1, 0, 0, 0), (geo_obs_cost, 0, geo_ore_cost)))

    # obsidian
    obs_ore_cost, obs_clay_cost = get_obsidian_robot_cost(blueprint)
    if ore >= obs_ore_cost and clay >= obs_clay_cost:
        choices.append(((0, 1, 0, 0), (0, obs_clay_cost, obs_ore_cost)))

    # clay
    if ore >= get_clay_robot_cost(blueprint):
        choices.append(((0, 0, 1, 0), (0, 0, get_clay_robot_cost(blueprint))))

    # ore
    if ore >= get_ore_robot_cost(blueprint):
        choices.append(((0,0,0,1), (0, 0, get_ore_robot_cost(blueprint))))

    return choices

def get_max_geodes(num_geode_robots, time):
    # current production
    total = num_geode_robots * time

    # possible to build 1 every time
    for i in range(time, -1, -1):
        total += i

    return total


calls = 0

def get_possible_next_states(blueprint, num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, geode, obsidian, clay, ore, time):

    states = []

    global calls

    calls += 1
    if calls % 100000 == 0:
        print(calls)

    new_geode = geode + num_geode_robots
    new_obsidian = obsidian + num_obsidian_robots
    new_clay = clay + num_clay_robots
    new_ore = ore + num_ore_robots

    # build nothing
    states.append((num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, new_geode, new_obsidian, new_clay, new_ore, time-1))

    # build something
    for benefit, cost in get_build_choices(blueprint, obsidian, clay, ore):
        states.append((num_geode_robots + benefit[0],
                        num_obsidian_robots + benefit[1],
                        num_clay_robots + benefit[2],
                        num_ore_robots + benefit[3],
                        new_geode,
                        new_obsidian - cost[0],
                        new_clay - cost[1],
                        new_ore - cost[2],
                        time - 1))

    return states


current_min_states = {(0, 0, 0, 1, 0, 0, 0, 0, 24)}

fct = []

for i in range(0, 6):
    fct.append(math.factorial(i))


best_so_far = 0

def have_completely_better_state(new_state, states, time):
    global best_so_far

    best_so_far = max(new_state[4], best_so_far)

    if time < 5 and fct[time] + new_state[4] < best_so_far:
        return True

    for state in states:
        if state is new_state:
            continue

        better_than = False

        for i in range(len(state)):
            if new_state[i] > state[i]:
                better_than = True
                break

        if better_than:
            continue

        return True

    return False


def prune_beaten_states(base_states, new_states):
    # num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, new_geode, new_obsidian, new_clay, new_ore
    super_map = [{} for _ in range(8)]

    print("super start", time.time())
    for base_state in base_states:
        key = hash(base_state)

        for i in range(4):
            v1 = base_state[i]
            v2 = base_state[i+4]

            for j in range(v1+1):
                for k in range(v2 + 1):
                    if (j, k) not in super_map[i]:
                        super_map[i][(j, k)] = set()

                    super_map[i][(j, k)].add(key)

    print("super fin", time.time())

    passed_states = set()

    print("comp start", time.time())
    for new_state in new_states:
        key = hash(new_state)
        passed = False


        sets = []

        for i in range(4):
            i1 = i
            i2 = i + 4
            i_key = (new_state[i1], new_state[i2])

            if i_key not in super_map[i]:
                passed_states.add(new_state)
                passed = True
                break

            sets.append(super_map[i][i_key])

        if passed:
            continue

        possible_beats = sets[0].intersection(*sets[1:])

        if len(possible_beats) == 0 or (len(possible_beats) == 1 and key in possible_beats):
            passed_states.add(new_state)
            continue

    print("comp fin", time.time())

    return passed_states


def add_to_current_super_map(super_map, super_map_key_to_val, state):
    key = hash(state)
    super_map_key_to_val[key] = state

    for i in range(2):
        v1 = state[i]
        v2 = state[i + 1]

        for j in range(v1 + 1):
            for k in range(v2 + 1):
                if (j, k) not in super_map[i]:
                    super_map[i][(j, k)] = set()

                super_map[i][(j, k)].add(key)


def beats_super_map(super_map, super_map_key_to_val, state):
    key = hash(state)

    sets = []

    for i in range(2):
        i1 = i
        i2 = i + 1
        i_key = (state[i1], state[i2])

        if i_key not in super_map[i]:
            return True

        sets.append(super_map[i][i_key])

    possible_beats = sets[0].intersection(*sets[1:])

    for possible_beat in possible_beats:
        if super_map_key_to_val[key] == state:
            continue

        for i in range(8):
            if super_map_key_to_val[possible_beat][i] < state[i]:
                continue

        return False

    return True


super_map = {i: {} for i in range(4)}
super_map_key_to_val = {}
add_to_current_super_map(super_map, super_map_key_to_val, (0, 0, 0, 1, 0, 0, 0, 0, 24))


for i in range(23, -1, -1):
    print(i, len(current_min_states), len(super_map[0]), len(super_map[1]), len(super_map[2]), len(super_map[3]))

    new_current_min_states = set()

    for state in current_min_states:
        for new_state in get_possible_next_states(blueprints[1], *state):
            if beats_super_map(super_map, super_map_key_to_val, new_state):
                add_to_current_super_map(super_map, super_map_key_to_val, new_state)
                new_current_min_states.add(new_state)

    current_min_states = new_current_min_states


max_geodes = 0

for state in current_min_states:
    max_geodes = max(max_geodes, state[4])

print(max_geodes)