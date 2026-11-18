def two_sum_first_pair(nums, target):
    """Return [i, j] for the first pair of positions that add up to target, or [-1, -1]."""
    # This is correct but too slow: it checks every pair.
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return [-1, -1]
