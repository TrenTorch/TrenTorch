def longest_ones(nums, k):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if nums[i : j + 1].count(0) <= k:
                best = max(best, j - i + 1)
    return best
