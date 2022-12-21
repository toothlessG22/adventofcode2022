from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict

monkeys = {}


class Operator(Enum):
    ADD = 0
    MULTIPLY = 1
    SUBTRACT = 2
    DIVIDE = 3
    EQUAL = 4

class Monkey(ABC):
    @abstractmethod
    def eval(self, monkeys: Dict[str, Monkey], monkey_val_cache: Dict[str, int]):
        pass

class YellMonkey(Monkey):
    def __init__(self, key: str, val: int):
        self.key = key
        self.val = val

    def eval(self, monkeys: Dict[str, Monkey], monkey_val_cache: Dict[str, int]):
        if self.key in monkey_val_cache:
            return monkey_val_cache[self.key]

        monkey_val_cache[self.key] = self.val
        return self.val

    def __repr__(self):
        return str(self.val)


class OperatorMonkey(Monkey):
    def __init__(self, key: str, m1: str, m2: str, op: Operator):
        self.key = key
        self.m1 = m1
        self.m2 = m2
        self.op = op

    def eval(self, monkeys: Dict[str, Monkey], monkey_val_cache: Dict[str, int]):
        if self.key in monkey_val_cache:
            return monkey_val_cache[self.key]

        m1_val = monkeys[self.m1].eval(monkeys, monkey_val_cache)
        m2_val = monkeys[self.m2].eval(monkeys, monkey_val_cache)

        if self.op == Operator.ADD:
            result = m1_val + m2_val
        elif self.op == Operator.MULTIPLY:
            result = m1_val * m2_val
        elif self.op == Operator.DIVIDE:
            result = m1_val // m2_val
        elif self.op == Operator.SUBTRACT:
            result = m1_val - m2_val
        elif self.op == Operator.EQUAL:
            print(m1_val, m2_val)
            result = 1 if m1_val == m2_val else 0
        else:
            assert False

        monkey_val_cache[self.key] = result
        return result

    def __repr__(self):
        return f"{self.m1} {self.op} {self.m2}"


monkeys = {}
monkey_val_cache = {}

with open("input.txt") as f:
    for line in f.readlines():
        line = line.strip()

        key = line[0:4]

        if "+" in line or "-" in line or "/" in line or "*" in line:
            m1 = line[6:10]
            m2 = line[13:]

            if "+" in line:
                op = Operator.ADD
            elif "-" in line:
                op = Operator.SUBTRACT
            elif "/" in line:
                op = Operator.DIVIDE
            elif "*" in line:
                op = Operator.MULTIPLY
            else:
                assert False

            monkeys[key] = OperatorMonkey(key, m1, m2, op)

        else:
            val = int(line[6:])

            monkeys[key] = YellMonkey(key, val)
# part 1
# print(monkeys["root"].eval(monkeys, monkey_val_cache))

# print(monkeys[monkeys["root"].m2].eval(monkeys, monkey_val_cache))

target_val = 0

root = monkeys["root"]
root.op = Operator.EQUAL

path = []
target_vals = []


def calc_new_m1_target_val(target_val, m2, operator):
    if operator == Operator.ADD:
        return target_val - m2
    elif operator == Operator.MULTIPLY:
        return target_val // m2
    elif operator == Operator.DIVIDE:
        return target_val * m2
    elif operator == Operator.SUBTRACT:
        return target_val - m2
    elif operator == Operator.EQUAL:
        return m2
    else:
        assert False


def calc_new_m2_target_val(target_val, m1, operator):

    if operator == Operator.ADD:
        return target_val - m1
    elif operator == Operator.MULTIPLY:
        return target_val // m1
    elif operator == Operator.DIVIDE:
        return m1 // target_val
    elif operator == Operator.SUBTRACT:
        return m1 - target_val
    elif operator == Operator.EQUAL:
        return m1
    else:
        assert False


while root.key != "humn":
    path.append(root)
    target_vals.append(target_val)

    tree_1_monkey_val_cache = {}
    tree_2_monkey_val_cache = {}


    if isinstance(root, YellMonkey):
        assert False

    tree_1_val = monkeys[root.m1].eval(monkeys, tree_1_monkey_val_cache)
    tree_2_val = monkeys[root.m2].eval(monkeys, tree_2_monkey_val_cache)
    op = root.op

    if "humn" in tree_1_monkey_val_cache and "humn" not in tree_2_monkey_val_cache:
        root = monkeys[root.m1]
        if root.key == "humn":
            break

        target_val = calc_new_m1_target_val(target_val, tree_2_val, op)
    elif "humn" in tree_2_monkey_val_cache and "humn" not in tree_1_monkey_val_cache:
        root = monkeys[root.m2]
        if root.key == "humn":
            break

        target_val = calc_new_m2_target_val(target_val, tree_1_val, op)
    else:
        assert False

print(target_vals[-1])
print(path[-1])

monkey_val_cache = {}
print(monkeys["root"].eval(monkeys, monkey_val_cache))


for i in range(-100000, 100000):
    monkeys["humn"] = YellMonkey("humn", target_vals[-1] + i)

    monkey_val_cache = {}
    if monkeys["root"].eval(monkeys, monkey_val_cache) == 1:
        print(target_vals[-1] + i)

        break

pass