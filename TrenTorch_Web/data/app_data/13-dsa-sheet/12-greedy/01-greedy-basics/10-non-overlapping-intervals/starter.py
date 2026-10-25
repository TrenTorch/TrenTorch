def erase_overlap(intervals: list[list[int]]) -> int:
    """Return the fewest intervals to remove so that none overlap."""
    # This is correct but too slow: it finds the longest chain of non-overlapping intervals with a double loop.
    items = sorted(intervals, key=lambda it: it[1])
    n = len(items)
    best = [1] * n
    for i in range(n):
        for j in range(i):
            if items[j][1] <= items[i][0] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return n - max(best, default=0)
