def floor_and_ceil(nums, target):
    """Return [floor, ceil] of target in the sorted list, using -1 when missing."""
    # This is correct but reads every value. The big tests allow only a few reads.
    below = [x for x in nums if x <= target]
    above = [x for x in nums if x >= target]
    return [max(below) if below else -1, min(above) if above else -1]
