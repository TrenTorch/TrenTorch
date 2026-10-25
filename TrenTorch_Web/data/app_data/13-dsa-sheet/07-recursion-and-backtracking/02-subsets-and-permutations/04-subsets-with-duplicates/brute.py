from itertools import combinations


def subsets_with_duplicates(nums):
    a = sorted(nums)
    found = {c for r in range(len(a) + 1) for c in combinations(a, r)}
    return [list(c) for c in sorted(found)]
