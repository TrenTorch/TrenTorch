def count_inversions(nums):
    """Return the number of pairs i < j with nums[i] > nums[j]."""
    # This is correct but too slow: it checks every pair.
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                count += 1
    return count
