def longest_within_limit(nums, limit):
    best = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            window = nums[i : j + 1]
            if max(window) - min(window) <= limit:
                best = max(best, j - i + 1)
    return best
