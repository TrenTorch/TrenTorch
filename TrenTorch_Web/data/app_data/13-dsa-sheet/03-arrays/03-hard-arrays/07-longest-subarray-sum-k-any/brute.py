def longest_subarray_sum_k_any(nums, k):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                best = max(best, j - i + 1)
    return best
