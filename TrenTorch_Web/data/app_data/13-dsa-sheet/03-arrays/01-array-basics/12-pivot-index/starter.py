def pivot_index(nums):
    """Return the leftmost index with equal sums on both sides, or -1."""
    # This is correct but too slow: it adds up both sides for every index.
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1 :]):
            return i
    return -1
