from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

@dataclass
class Input:
    rules: list[tuple[int, int]]
    updates: list[list[int]]


def parse(lines: list[str]) -> Input:
    it = iter(lines)

    rules: list[tuple[int, int]] = []
    updates: list[list[int]] = []

    while l := next(it):
        rules.append(tuple(int(s) for s in l.split('|')))

    for l in it:
        updates.append([int(s) for s in l.split(',')])

    return Input(rules, updates)


SAMPLE = parse("""\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".splitlines())

DATA = parse([l.strip() for l in open('05/input.txt').readlines()])

# Problem 1

def to_graph(rules: list[tuple[int, int]]) -> dict[int, list[int]]:
    graph = defaultdict[int, list[int]](list)

    for before, after in rules:
        graph[after].append(before)

    # an ugly hack to ensure that the graph is fully populated
    # otherwise it mutates during iteration and all hell goes loose
    for n, deps in dict(graph).items():
        for d in deps:
            if not d in graph:
                graph[d] = []

    return graph

# DFS-based topological sort, stolen here https://llego.dev/posts/implementing-topological-sort-python/
def toposort(graph: dict[int, list[dict]]):
    visited = set[int]() # Track visited nodes
    topological_order: list[int] = [] # Store topological order

    def topological_sort_dfs(graph: dict[int, list[dict]], node: int):
        visited.add(node)

        #if node in graph:
        for neighbor in graph[node]:
            if neighbor not in visited:
                topological_sort_dfs(graph, neighbor)
        topological_order.append(node)

    for node in graph:
        if node not in visited:
            topological_sort_dfs(graph, node)

    return topological_order

def find_errors(sorted: list[int], update: list[int]) -> Iterable[int]:
    start = 0
    for i in range(0, len(update)):
        n = update[i]
        if not n in sorted:
            continue
        try:
            start = sorted.index(n, start)
        except ValueError:
            yield i

def is_correct(sorted: list[int], update: list[int]) -> bool:
    # start = 0

    # for n in update:
    #     if not n in sorted:
    #         continue
    #     try:
    #         start = sorted.index(n, start)
    #     except ValueError:
    #         return False
                
    # return True
    return len(list(find_errors(sorted, update))) == 0

def find_good_updates(data: Input) -> Iterable[list[int]]:

    for u in data.updates:
        applicable_rules = [(a,b) for (a,b) in data.rules if a in u
                            ]
        sorted_rules = toposort(to_graph(applicable_rules))
        if is_correct(sorted_rules, u):
            yield u

def sum_middles(updates: list[list[int]]) -> int:
    def mid(u: list[int]):
        return u[len(u)//2]
    return sum(mid(u) for u in updates)

def problem1(data: Input) -> int:
    return sum_middles(find_good_updates(data))

assert problem1(SAMPLE) == 143
print("Problem 1: ", problem1(DATA))

# Problem 2

def fix(data: Input) -> Iterable[list[int]]:
    correct = list(find_good_updates(data))
    incorrect = [ u for u in data.updates if not u in correct ]

    for u in incorrect:
        applicable_rules = [(a,b) for (a,b) in data.rules if a in u
                        ]
        sorted_rules = toposort(to_graph(applicable_rules))

        error_spots = list(find_errors(sorted_rules, u))
        while error_spots:
            spot = error_spots.pop()
            val = u[spot]
            u.pop(spot)
            for i in range(0, len(u)):
                attempt = list(u)   # copy
                attempt.insert(i, val)
                new_spots = list(find_errors(sorted_rules, attempt))
                if len(new_spots) <= len(error_spots):
                    u = attempt
                    error_spots = new_spots
                    break
        yield u


def problem2(data: Input) -> bool:
    return sum_middles(fix(data))

assert problem2(SAMPLE) == 123

print("Problem 2: ", problem2(DATA))
