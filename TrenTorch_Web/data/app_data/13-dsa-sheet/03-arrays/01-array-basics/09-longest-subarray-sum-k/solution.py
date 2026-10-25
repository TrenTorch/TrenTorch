def longest_subarray_sum_k(nums, k):
    best = left = total = 0
    for right, x in enumerate(nums):
        total += x
        while total > k and left <= right:
            total -= nums[left]
            left += 1
        if total == k:
            best = max(best, right - left + 1)
    return best
