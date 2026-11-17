def longest_subarray_sum_k_any(nums, k):
    """Return the length of the longest run of nums that adds up to k."""
    # This is correct but too slow: it tries every start and end.
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                best = max(best, j - i + 1)
    return best
