from itertools import combinations_with_replacement


def combination_sum(candidates, target):
    a = sorted(candidates)
    found = set()
    longest = target // a[0] if a else 0
    for r in range(1, longest + 1):
        for c in combinations_with_replacement(a, r):
            if sum(c) == target:
                found.add(c)
    return [list(c) for c in sorted(found)]
