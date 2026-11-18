from itertools import combinations


def all_combinations(n, k):
    return [list(c) for c in combinations(range(1, n + 1), k)]
