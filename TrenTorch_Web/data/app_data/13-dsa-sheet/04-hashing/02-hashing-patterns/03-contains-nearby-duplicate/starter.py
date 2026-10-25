def contains_nearby_duplicate(nums, k):
    """Return True if two equal values are at most k positions apart."""
    # This is correct but too slow: it compares every pair of positions.
    for i in range(len(nums)):
        for j in range(i + 1, min(len(nums), i + k + 1)):
            if nums[i] == nums[j]:
                return True
    return False
