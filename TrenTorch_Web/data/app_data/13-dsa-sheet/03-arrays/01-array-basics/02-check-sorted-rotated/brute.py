def check_sorted_rotated(nums):
    target = sorted(nums)
    return any(nums[k:] + nums[:k] == target for k in range(len(nums)))
