from itertools import combinations


def four_sum(nums, target):
    """Return all different groups of four values that add up to target."""
    # This is correct but too slow: it tries every group of four positions.
    found = {c for c in combinations(sorted(nums), 4) if sum(c) == target}
    return [list(c) for c in sorted(found)]
