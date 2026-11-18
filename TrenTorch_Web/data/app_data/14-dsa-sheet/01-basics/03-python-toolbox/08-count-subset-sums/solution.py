from collections import Counter


def _sums_by_size(values):
    # (size, sum) -> number of subsets of `values` with that size and sum
    states = Counter({(0, 0): 1})
    for v in values:
        for (size, total), ways in list(states.items()):
            states[(size + 1, total + v)] += ways
    return states


def count_subset_sums(nums, k, target):
    half = len(nums) // 2
    left = _sums_by_size(nums[:half])
    right = _sums_by_size(nums[half:])
    count = 0
    for (size, total), ways in right.items():
        count += ways * left.get((k - size, target - total), 0)
    return count
