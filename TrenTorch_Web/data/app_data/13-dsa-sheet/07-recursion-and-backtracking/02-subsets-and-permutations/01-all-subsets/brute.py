from itertools import combinations


def all_subsets(nums):
    a = sorted(nums)
    return sorted([list(c) for r in range(len(a) + 1) for c in combinations(a, r)])
