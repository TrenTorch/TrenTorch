def allocate_books(pages, students):
    if students > len(pages):
        return -1
    lo, hi = max(pages), sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        needed, load = 1, 0
        for p in pages:
            if load + p > mid:
                needed += 1
                load = 0
            load += p
        if needed <= students:
            hi = mid
        else:
            lo = mid + 1
    return lo
