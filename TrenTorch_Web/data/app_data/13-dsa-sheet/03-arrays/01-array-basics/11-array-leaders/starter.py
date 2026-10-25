def array_leaders(nums):
    """Return the values that are bigger than everything to their right."""
    # This is correct but too slow: it compares every value with everything after it.
    out = []
    for i in range(len(nums)):
        if all(nums[i] > nums[j] for j in range(i + 1, len(nums))):
            out.append(nums[i])
    return out
