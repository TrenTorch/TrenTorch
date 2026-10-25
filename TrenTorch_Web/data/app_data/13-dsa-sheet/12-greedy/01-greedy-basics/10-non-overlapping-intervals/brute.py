def erase_overlap(intervals):
    n = len(intervals)
    best = 0
    for mask in range(1 << n):
        kept = sorted(intervals[i] for i in range(n) if mask >> i & 1)
        if all(kept[k][1] <= kept[k + 1][0] for k in range(len(kept) - 1)):
            best = max(best, len(kept))
    return n - best
