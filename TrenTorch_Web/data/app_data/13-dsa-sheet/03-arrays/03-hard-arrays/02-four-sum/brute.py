from itertools import combinations


def four_sum(nums, target):
    found = {c for c in combinations(sorted(nums), 4) if sum(c) == target}
    return [list(c) for c in sorted(found)]
