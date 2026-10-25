from itertools import combinations


def count_subset_sums(nums, k, target):
    return sum(1 for c in combinations(nums, k) if sum(c) == target)
