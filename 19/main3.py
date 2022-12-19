import re
from functools import lru_cache

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
    blueprints.append(tuple(blueprint))


def can_build_ore(blueprint, obsidian, clay, ore):
    return ore >= get_ore_robot_cost(blueprint)

def can_build_clay(blueprint, obsidian, clay, ore):
    return ore >= get_clay_robot_cost(blueprint)

def can_build_obsidian(blueprint, obsidian, clay, ore):
    obs_ore_cost, obs_clay_cost = get_obsidian_robot_cost(blueprint)
    return ore >= obs_ore_cost and clay >= obs_clay_cost

def can_build_geode(blueprint, obsidian, clay, ore):
    geo_ore_cost, geo_obs_cost = get_geode_robot_cost(blueprint)
    return ore >= geo_ore_cost and obsidian >= geo_obs_cost

def get_build_choices(blueprint, obsidian, clay, ore, bc_cache):
    key = (obsidian, clay, ore)

    if key in bc_cache:
        return bc_cache[key]

    choices = []

    # geode
    geo_ore_cost, geo_obs_cost = get_geode_robot_cost(blueprint)
    if ore >= geo_ore_cost and obsidian >= geo_obs_cost:
        choices.append((
            1, 0, 0, 0,
            0, -geo_obs_cost, 0, -geo_ore_cost))

    # obsidian
    obs_ore_cost, obs_clay_cost = get_obsidian_robot_cost(blueprint)
    if ore >= obs_ore_cost and clay >= obs_clay_cost:
        choices.append((
            0, 1, 0, 0,
            0, 0, -obs_clay_cost, -obs_ore_cost))

    # clay
    if ore >= get_clay_robot_cost(blueprint):
        choices.append((
            0, 0, 1, 0,
            0, 0, 0, -get_clay_robot_cost(blueprint)))

    # ore
    if ore >= get_ore_robot_cost(blueprint):
        choices.append((
            0, 0, 0, 1,
            0, 0, 0, -get_ore_robot_cost(blueprint)))

    bc_cache[key] = choices

    return choices

def apply_state_update(update, state):
    return (
        update[0] + state[0],
        update[1] + state[1],
        update[2] + state[2],
        update[3] + state[3],
        update[4] + state[4],
        update[5] + state[5],
        update[6] + state[6],
        update[7] + state[7],
    )


def passes_fake_sim(blueprint, state, time, target):
    num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, geode, obsidian, clay, ore = state

    _, obs_clay_cost = get_obsidian_robot_cost(blueprint)
    geo_ore_cost, geo_obs_cost = get_geode_robot_cost(blueprint)

    for t in range(time, 0, -1):
        is_building_geode = can_build_geode(blueprint, obsidian, clay, ore)
        is_building_obsidian = can_build_obsidian(blueprint, obsidian, clay, ore)

        obsidian_update = obsidian + num_obsidian_robots
        ore_update = ore + num_ore_robots
        if is_building_geode:
            obsidian_update -= geo_obs_cost

        clay_update = num_clay_robots
        if is_building_obsidian:
            clay_update -= obs_clay_cost

        update = (
            1 if is_building_geode else 0,
            1 if is_building_obsidian else 0,
            1 if can_build_clay(blueprint, obsidian, clay, ore) else 0,
            1 if can_build_ore(blueprint, obsidian, clay, ore) else 0,
            num_geode_robots,
            obsidian_update,
            clay_update,
            ore_update)
        state = apply_state_update(update, state)

        num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, geode, obsidian, clay, ore = state
        if geode + (t-1) * num_geode_robots > target:
            return True

    return False


print(passes_fake_sim(blueprints[0], (0, 2, 5, 1, 0, 9, 18, 3), 2, 0))
print(passes_fake_sim(blueprints[0], (0, 2, 5, 1, 0, 9, 18, 3), 1, 0))
print(passes_fake_sim(blueprints[0], (0, 2, 7, 1, 0, 7, 60, 2), 2, 0))

calls = 0
state_cache_hits = 0
best_time_cache_hits = 0
hardcode_hits = 0
best_geode_hits = 0
best_geode_hit_times = {}

def back_track(blueprint, state, time, cache, bc_cache, best_time_cache, best_geode_cache):
    num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots, geode, obsidian, clay, ore = state

    global calls
    global state_cache_hits
    global best_time_cache_hits
    global hardcode_hits
    global best_geode_hits
    global best_geode_hit_times

    calls += 1

    if calls % 100000 == 0:
        print("calls", calls, "state_cache", state_cache_hits, "best_time_cache", best_time_cache_hits, "harcode_hits", hardcode_hits, "best_geode", best_geode_hits, best_geode_hit_times,  best_geode_cache[0])

    if time == 1:
        hardcode_hits += 1
        best_geode_cache[0] = max(best_geode_cache[0], geode + num_geode_robots)
        return geode + num_geode_robots

    if state in cache:
        if time in cache[state]:
            state_cache_hits += 1
            return cache[state][time]
    else:
        cache[state] = {}

    if state in best_time_cache:
        if best_time_cache[state] > time:
            best_time_cache_hits += 1
            return -1

    best_time_cache[state] = time

    if time < 24:
        if not passes_fake_sim(blueprint, state, time, best_geode_cache[0]):
            best_geode_hits += 1
            if time not in best_geode_hit_times:
                best_geode_hit_times[time] = 0
            best_geode_hit_times[time] += 1
            cache[state][time] = -1
            return -1

    if time == 28:
        print(state)

    # ore_ore_cost = get_ore_robot_cost(blueprint)
    # clay_ore_cost = get_clay_robot_cost(blueprint)
    # obs_ore_cost, obs_clay_cost = get_obsidian_robot_cost(blueprint)
    # geo_ore_cost, geo_obs_cost = get_geode_robot_cost(blueprint)

    resource_update = (0, 0, 0, 0, num_geode_robots, num_obsidian_robots, num_clay_robots, num_ore_robots)
    resource_updated_state = apply_state_update(resource_update, state)

    best = 0

    build_choices = get_build_choices(blueprint, obsidian, clay, ore, bc_cache)

    for build_choice in build_choices:
        best = max(best, back_track(blueprint, apply_state_update(build_choice, resource_updated_state), time-1, cache, bc_cache, best_time_cache, best_geode_cache))

    if len(build_choices) != 4:
        best = max(best, back_track(blueprint, resource_updated_state, time-1, cache, bc_cache, best_time_cache, best_geode_cache))

    cache[state][time] = best

    return best

for i in range(len(blueprints)):
    print(i, back_track(blueprints[i], (0, 0, 0, 1, 0, 0, 0, 0), 32, {}, {}, {}, [0]))

