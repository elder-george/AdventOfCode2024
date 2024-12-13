
from dataclasses import dataclass
import dataclasses
from enum import Enum


class GuardDir(Enum):
    UP = '^'
    DOWN = 'v'
    RIGHT = '>'
    LEFT = '<'

delta_for = {
    GuardDir.UP: (0, -1),
    GuardDir.DOWN: (0, 1),
    GuardDir.RIGHT: (1, 0),
    GuardDir.LEFT: (-1, 0),
}

turned = {
    GuardDir.UP: GuardDir.RIGHT,
    GuardDir.DOWN: GuardDir.LEFT,
    GuardDir.RIGHT: GuardDir.DOWN,
    GuardDir.LEFT: GuardDir.UP,

}

@dataclass
class Map:
    width: int
    height: int
    objects: set[tuple[int, int]]
    guard_pos: tuple[int, int]
    guard_dir: GuardDir

    @staticmethod
    def parse(lines: list[str]) -> 'Map':
        height = len(lines)
        width = len(lines[0])

        objects: set[tuple[int, int]] = set()

        for y, l in enumerate(lines):
            for x, tile in enumerate(l):
                if tile == '.':
                    continue
                elif tile == '#':
                    objects.add((x,y))
                else:
                    guard_dir = GuardDir(tile)
                    guard_pos = (x, y)

        return Map(width, height, objects, guard_pos, guard_dir)

SAMPLE_MAP = Map.parse([l.strip() for l in """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()])

assert(SAMPLE_MAP.width == 10)
assert(SAMPLE_MAP.height == 10)
assert(len(SAMPLE_MAP.objects) == 8)
assert(SAMPLE_MAP.guard_dir == GuardDir.UP)
assert(SAMPLE_MAP.guard_pos == (4, 6))

REAL_MAP = Map.parse([l.strip() for l in open('06/input.txt').readlines()])

def make_one_turn(map: Map):
    dx, dy = delta_for[map.guard_dir]

    x, y = map.guard_pos
    x += dx
    y += dy

    if (x,y) in map.objects:
        map.guard_dir = turned[map.guard_dir]
    else:
        x,y = map.guard_pos 
        map.guard_pos = (x+dx, y+dy)
        if not (0 <= x < map.width) or not (0 <= y < map.height):
            return False
        
    return True

def track_positions(data: Map) -> set[tuple[int, int]]:
    positions: set[tuple[int, int]] = set()
    positions.add(data.guard_pos)

    while make_one_turn(data):
        positions.add(data.guard_pos)

    return list(positions)


def problem1(data: Map) -> int:
    return len(track_positions(dataclasses.replace(data))) - 1

assert problem1(SAMPLE_MAP) == 41
print( problem1(REAL_MAP) )