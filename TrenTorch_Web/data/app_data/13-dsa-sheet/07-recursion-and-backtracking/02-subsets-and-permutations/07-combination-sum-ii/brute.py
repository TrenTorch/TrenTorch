from itertools import combinations


def combination_sum_ii(candidates, target):
    a = sorted(candidates)
    found = {
        c for r in range(1, len(a) + 1) for c in combinations(a, r) if sum(c) == target
    }
    return [list(c) for c in sorted(found)]
