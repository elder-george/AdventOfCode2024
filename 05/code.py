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
# print(DATA.rules)

def to_graph(rules: list[tuple[int, int]]) -> dict[int, list[int]]:
    graph = defaultdict[int, list[int]](list)

    for before, after in rules:
        graph[after].append(before)

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

def is_correct(sorted: list[int], rule: list[int]) -> bool:
    start = 0

    for n in rule:
        if not n in sorted:
            continue
        try:
            start = sorted.index(n, start)
        except ValueError:
            return False
                
    return True

def find_good_updates(data: Input) -> Iterable[list[int]]:

    for u in data.updates:
        applicable_rules = [(a,b) for (a,b) in data.rules if a in u
                            ]
        sorted_data = toposort(to_graph(applicable_rules))
        if is_correct(sorted_data, u):
            yield u

def problem1(data: Input) -> int:
    def mid(u: list[int]):
        return u[len(u)//2]
    return sum(mid(u) for u in find_good_updates(data))

assert problem1(SAMPLE) == 143
print("Problem 1: ", problem1(DATA))