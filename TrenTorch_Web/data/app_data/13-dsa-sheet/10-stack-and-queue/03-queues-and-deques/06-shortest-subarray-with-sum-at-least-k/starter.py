def shortest_subarray_sum_k(nums: list[int], k: int) -> int:
    """Return the length of the shortest subarray with sum at least k, or -1."""
    # This is correct but too slow: it tries every subarray.
    best = -1
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= k:
                if best == -1 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best
