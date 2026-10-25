def floor_and_ceil(nums, target):
    below = [x for x in nums if x <= target]
    above = [x for x in nums if x >= target]
    return [max(below) if below else -1, min(above) if above else -1]
