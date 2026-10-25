def rob_circle(nums):
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        if mask & (mask >> 1) or (n > 1 and mask & 1 and mask >> (n - 1) & 1):
            continue
        best = max(best, sum(nums[i] for i in range(n) if mask >> i & 1))
    return best
