def count_reverse_pairs(nums):
    """Return the number of pairs i < j with nums[i] > 2 * nums[j]."""
    # This is correct but too slow: it checks every pair.
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > 2 * nums[j]:
                count += 1
    return count
