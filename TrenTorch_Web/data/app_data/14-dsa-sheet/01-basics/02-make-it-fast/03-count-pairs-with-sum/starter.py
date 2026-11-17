def count_pairs_with_sum(nums, target):
    """Return how many pairs i < j have nums[i] + nums[j] == target."""
    # This is correct but too slow: it checks every pair.
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                count += 1
    return count
