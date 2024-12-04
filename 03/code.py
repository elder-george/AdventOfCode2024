import re
from typing import Iterable

SAMPLE_DATA = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

DATA = open('03/input.txt').read()

def extract(s: str) -> list[tuple[int, int]]:
    return [
        (int(m.group('A')), int(m.group('B'))) for m in (re.finditer(r"mul\((?P<A>\d+),(?P<B>\d+)\)", s))
    ]

assert extract(SAMPLE_DATA) == [(2,4), (5,5), (11,8), (8,5)]

# problem 1
def problem1(data: str) -> int:
    return sum(a*b for a,b in extract(data))

assert problem1(SAMPLE_DATA) == 161

print("Problem 1: ", problem1(DATA))

# problem 2

def extract_conditionally(s: str) -> Iterable[tuple[int, int]]:
    enabled = True
    for m in re.finditer(r"(?P<FLAG>do(n't)?\(\))|(mul\((?P<A>\d+),(?P<B>\d+)\))", s):
        if m.group('FLAG'):
            enabled = m.group('FLAG') == 'do()'
        elif enabled:
            yield int(m.group('A')), int(m.group('B'))

def problem2(data: str):
    return sum(a*b for a,b in extract_conditionally(data))

assert 48 == problem2(SAMPLE_DATA)
print("Problem 2: ", problem2(DATA))