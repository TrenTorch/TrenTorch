def min_subarray_len(target: int, nums: list[int]) -> int:
    """Return the length of the shortest subarray with sum at least target, or 0."""
    # This is correct but too slow: it tries every start and extends until the sum is big enough.
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best
