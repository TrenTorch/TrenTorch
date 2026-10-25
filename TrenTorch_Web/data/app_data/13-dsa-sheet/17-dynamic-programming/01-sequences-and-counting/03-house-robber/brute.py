def rob(nums):
    best = 0
    for mask in range(1 << len(nums)):
        if mask & (mask >> 1):
            continue
        best = max(best, sum(nums[i] for i in range(len(nums)) if mask >> i & 1))
    return best
