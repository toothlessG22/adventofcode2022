import re
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


def solve(blueprint, num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, geode, obsidian, clay, ore, time):

    time = time - 1

    if time == 0:
        return geode + num_geode_robots

    ore_ore_cost = get_ore_robot_cost(blueprint)
    clay_ore_cost = get_clay_robot_cost(blueprint)
    obs_ore_cost, obs_clay_cost = get_obsidian_robot_cost(blueprint)
    geo_ore_cost, geo_obs_cost = get_geode_robot_cost(blueprint)

    if time == 1:
        if ore < geo_ore_cost or obsidian < geo_obs_cost:
            # can't build geode so return geodes
            return geode + num_geode_robots * 2
        else:
            return geode + num_geode_robots * 2 + 1

    if time == 2:
        # Build geode NOW <- if we have enough to build a geode we should do it now
        if ore >= geo_ore_cost and obsidian >= geo_obs_cost:
            # we have enough production to do a double build of geode <- ignorable at 24
            if ore + num_ore_robots - geo_ore_cost >= geo_ore_cost and obsidian + num_obsidian_robots - geo_obs_cost >= geo_obs_cost:
                return geode + num_geode_robots * 3 + 2 + 1

            # we don't
            else:
                return geode + num_geode_robots * 3 + 2

        # Build obsidian to get geode at 1
        if ore + num_ore_robots >= geo_ore_cost and obsidian + num_obsidian_robots + 1 == geo_obs_cost:
            return geode + num_geode_robots * 3 + 1

        # Build ore to get geode at 1 <- this actually doesn't matter because we need at least 2 turns for ore to break even

        # do nothing because in the end it doesn't even matter
        return geode + num_geode_robots * 3


x = solve(blueprints[0], 1, 2, 3, 3, 1, 12, 0, 3, 2)

print(x)

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

    # always build something if we have the option to build something
    if len(states) != 4:
        # build nothing
        states.append((num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, new_geode, new_obsidian,
                       new_clay, new_ore, time - 1))

    return states


def add_to_super_map(super_map, state):
    for i in range(0, state[0]+1):
        if i not in super_map:
            super_map[i] = {}
        for j in range(0, state[1]+1):
            if j not in super_map[i]:
                super_map[i][j] = {}
            for k in range(0, state[2]+1):
                if k not in super_map[i][j]:
                    super_map[i][j][k] = {}
                for l in range(0, state[3]+1):
                    if l not in super_map[i][j][k]:
                        super_map[i][j][k][l] = {}
                    for m in range(0, state[4]+1):
                        if m not in super_map[i][j][k][l]:
                            super_map[i][j][k][l][m] = {}
                        for n in range(0, state[5]+1):
                            if n not in super_map[i][j][k][l][m]:
                                super_map[i][j][k][l][m][n] = {}
                            for o in range(0, state[6]+1):
                                if o not in super_map[i][j][k][l][m][n]:
                                    super_map[i][j][k][l][m][n][o] = {}
                                for p in range(0, state[7]+1):
                                    if p not in super_map[i][j][k][l][m][n][o]:
                                        super_map[i][j][k][l][m][n][o][p] = {}


def beats_super_map(super_map, state):
    s = super_map

    for i in range(8):
        if state[i] not in s:
            return True

        s = s[state[i]]

    return False


def back_to_basics(base_states, state):
    for base_state in base_states:
        if base_state is new_state:
            continue

        passed = True

        for i in range(8):
            if base_state[i] < state[i]:
                passed = True
                break

        if passed:
            break

        return False

    return True

ql = 0

for i in range(len(blueprints)):

    super_map = {}
    current_min_states = {(0, 0, 0, 1, 0, 0, 0, 0, 24)}
    add_to_super_map(super_map, (0, 0, 0, 1, 0, 0, 0, 0, 24))

    for j in range(24, 3, -1):
        print(j, len(current_min_states))

        new_current_min_states = set()

        for state in current_min_states:
            for new_state in get_possible_next_states(blueprints[i], *state):
                if back_to_basics(current_min_states, new_state):
                    new_current_min_states.add(new_state)

        current_min_states = set()

        for state in new_current_min_states:
            if back_to_basics(new_current_min_states, new_state):
                current_min_states.add(state)

    max_geodes = 0

    for state in current_min_states:

        if solve(blueprints[i], *state) > max_geodes:
            print(state)

        max_geodes = max(max_geodes, solve(blueprints[i], *state))

    print("Max", max_geodes)

    ql += max_geodes * (i+1)

print(ql)