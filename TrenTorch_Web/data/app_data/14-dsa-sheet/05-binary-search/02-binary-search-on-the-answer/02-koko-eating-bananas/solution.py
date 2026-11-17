def min_eating_speed(piles, hours):
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        needed = sum(-(-p // mid) for p in piles)
        if needed <= hours:
            hi = mid
        else:
            lo = mid + 1
    return lo
