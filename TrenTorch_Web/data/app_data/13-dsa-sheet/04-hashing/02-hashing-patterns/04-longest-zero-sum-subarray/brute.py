def longest_zero_sum_subarray(nums):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == 0:
                best = max(best, j - i + 1)
    return best
