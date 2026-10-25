def min_subarray_len(target, nums):
    best = len(nums) + 1
    total = 0
    left = 0
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
