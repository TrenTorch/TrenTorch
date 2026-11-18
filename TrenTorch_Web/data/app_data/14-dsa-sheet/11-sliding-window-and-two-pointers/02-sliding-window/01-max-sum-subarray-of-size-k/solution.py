def max_sum_k(nums, k):
    total = sum(nums[i] for i in range(k))
    best = total
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]
        best = max(best, total)
    return best
