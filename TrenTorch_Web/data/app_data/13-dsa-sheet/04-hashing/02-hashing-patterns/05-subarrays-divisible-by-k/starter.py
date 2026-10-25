def subarrays_divisible_by_k(nums, k):
    """Return how many contiguous runs of nums have a sum divisible by k."""
    # This is correct but too slow: it tries every start and end.
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total % k == 0:
                count += 1
    return count
