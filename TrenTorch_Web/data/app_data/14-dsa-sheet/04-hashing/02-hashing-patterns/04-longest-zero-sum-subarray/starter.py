def longest_zero_sum_subarray(nums):
    """Return the length of the longest run of nums that adds up to 0."""
    # This is correct but too slow: it tries every start and end.
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == 0:
                best = max(best, j - i + 1)
    return best
