def aggressive_cows(stalls, cows):
    s = sorted(stalls)

    def can_place(distance):
        placed, last = 1, s[0]
        for position in s[1:]:
            if position - last >= distance:
                placed += 1
                last = position
        return placed >= cows

    lo, hi = 1, s[-1] - s[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can_place(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo
