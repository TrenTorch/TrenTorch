def floor_and_ceil(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    ceil = nums[lo] if lo < len(nums) else -1
    if lo < len(nums) and nums[lo] == target:
        floor = target
    else:
        floor = nums[lo - 1] if lo > 0 else -1
    return [floor, ceil]
