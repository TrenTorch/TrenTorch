def count_subarrays_xor_k(nums, k):
    """Return how many contiguous runs of nums have a bitwise XOR equal to k."""
    # This is correct but too slow: it tries every start and end.
    count = 0
    for i in range(len(nums)):
        value = 0
        for j in range(i, len(nums)):
            value ^= nums[j]
            if value == k:
                count += 1
    return count
