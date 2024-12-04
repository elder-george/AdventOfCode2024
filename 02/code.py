import re
from typing import Optional

SAMPLE= """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9\
""".split('\n')

def parse(ls: list[str]) -> list[list[int]]:
    def parse_line(l: str) -> list[int]:
        return [ int(s) for s in re.findall(r"\d+", l)]
    return [parse_line(l) for l in ls]

SAMPLE_DATA = parse(SAMPLE)

DATA = parse(open('02/input.txt').readlines())

# problem 1
def is_monotonous(l: list[int]) -> bool:
    sign = 0

    for i in range(1, len(l)):
        diff = l[i] - l[i-1]
        if not (1 <= abs(diff) <= 3):
            return False
        diff = diff // abs(diff)
        if sign == 0:
            sign = diff
        elif sign != diff:
            return False
    
    return True

def problem1(ls: list[list[int]]) -> int:
    return sum(is_monotonous(l) for l in ls)


assert problem1(SAMPLE_DATA) == 2

print("Problem 1:", problem1(DATA))

# problem 2

# A very bad, naive solution
def is_almost_monotonous(l: list[int]) -> bool:
    if is_monotonous(l):
        return True
    
    for i in range(0, len(l)):
        l1 = l.copy()
        del l1[i]
        if is_monotonous(l1):
            return True
    
    return False

def problem2(ls: list[list[int]]) -> int:
    return sum(is_almost_monotonous(l) for l in ls)

assert 4 == problem2(SAMPLE_DATA)

print("Problem 2:", problem2(DATA))