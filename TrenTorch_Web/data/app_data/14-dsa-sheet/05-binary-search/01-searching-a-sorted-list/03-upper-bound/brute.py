def upper_bound(nums, target):
    for i, x in enumerate(nums):
        if x > target:
            return i
    return len(nums)
