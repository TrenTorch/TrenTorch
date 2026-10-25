def min_days_bouquets(bloom, m, k):
    if m * k > len(bloom):
        return -1

    def possible(day):
        bouquets = run = 0
        for b in bloom:
            if b <= day:
                run += 1
                if run == k:
                    bouquets += 1
                    run = 0
            else:
                run = 0
        return bouquets >= m

    lo, hi = min(bloom), max(bloom)
    while lo < hi:
        mid = (lo + hi) // 2
        if possible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
