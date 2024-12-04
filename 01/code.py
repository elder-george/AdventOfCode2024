import re
import collections


def parse(ls: list[str])-> list[tuple[int, int]]:
    return [ (int(A),int(B)) for A,B in (re.match(r"(?P<A>\d+)\s+(?P<B>\d+)", l).groups() for l in ls) ]

SAMPLE_DATA = parse("""\
3   4
4   3
2   5
1   3
3   9
3   3\
""".split("\n"))

DATA = parse(open('01/input.txt').readlines())

def col(ls: list[tuple], n: int) -> list[int]:
    return [t[n] for t in ls]

# Problem 1
def problem1(data: list[tuple[int, int]]):

    col1: list[int] = sorted(col(data, 0))
    col2:list[int] = sorted(col(data, 1))

    return sum( abs(a - b) for a, b in zip(col1, col2))

assert 11 == problem1(SAMPLE_DATA)

print(problem1(DATA))

def problem2(data: list[tuple[int, int]]) -> int:
    col1: list[int] = col(data, 0)
    col2: list[int] = col(data, 1)

    counts = collections.Counter(col2)
    return sum(n * counts[n] for n in col1)

print(problem2(SAMPLE_DATA))

assert 31 == problem2(SAMPLE_DATA)
print(problem2(DATA))
