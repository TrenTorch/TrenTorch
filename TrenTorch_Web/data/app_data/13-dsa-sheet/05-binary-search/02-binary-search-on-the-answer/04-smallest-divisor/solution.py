def smallest_divisor(nums, threshold):
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(-(-x // mid) for x in nums) <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return lo
