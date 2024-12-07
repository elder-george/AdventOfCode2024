
import enum
import re
from typing import Iterable


SAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX\
""".split('\n')

DATA = [l.strip() for l in  open('04/input.txt').readlines()]

# problem 1

class Orientation(enum.Enum):
    HOR = '-'
    VER = '|'
    UP = '/'
    DOWN = '\\'


def coords(data: list[str]) -> Iterable[tuple[int, int]]:
    for y in range(0, len(data)):
        for x in range(0, len(data[y])):
            yield x,y

def matches(data: list[str], word:str, x: int, y: int, dx: int, dy: int) -> bool:
    for i, c in enumerate(word):
        newX, newY = x + dx*i, y + dy*i
        if newX < 0 or newX >= len(data[0]) or newY < 0 or newY >= len(data):
            return False
        if data[newY][newX] != c:
            return False
        
    return True

def find_starts(data: list[str]) -> Iterable[tuple[int, int]]:
    for x, y in coords(data):
        if data[y][x] == 'X':
            for dx, dy in [(0,1), (0,-1), (-1, 0), (1,0), (1,1), (1,-1), (-1, 1), (-1, -1)]:
                if matches(data, 'XMAS', x, y, dx, dy):
                    yield (x, y)


def problem1(data: list[str]) -> int:
    return sum(1 for _ in find_starts(data))


assert problem1(SAMPLE) == 18
print(problem1(DATA))

# Problem 2

def find_mas(data: list[str]) -> Iterable[tuple[int, int]]:
    for x, y in coords(data):
        if (matches(data, 'MAS', x, y, 1, 1) or matches(data, 'SAM', x, y, 1, 1)) and\
            (matches(data, 'MAS', x, y+2, 1, -1) or matches(data, 'SAM', x, y+2, 1, -1)):
            yield (x,y)

def problem2(data: list[str]) -> int:
    return sum(1 for _ in find_mas(data))

assert problem2(SAMPLE) == 9
print(problem2(DATA))
