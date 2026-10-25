def count_subarrays_sum_k(nums, k):
    """Return how many contiguous runs of nums add up to k."""
    # This is correct but too slow: it tries every start and end.
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count
