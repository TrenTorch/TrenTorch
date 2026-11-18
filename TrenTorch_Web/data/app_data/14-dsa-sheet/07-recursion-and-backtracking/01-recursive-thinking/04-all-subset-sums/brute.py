from itertools import combinations


def all_subset_sums(nums):
    return sorted(sum(c) for r in range(len(nums) + 1) for c in combinations(nums, r))
