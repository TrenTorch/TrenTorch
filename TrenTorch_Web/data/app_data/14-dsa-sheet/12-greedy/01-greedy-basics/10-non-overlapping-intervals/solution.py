def erase_overlap(intervals):
    removed = 0
    last_end = None
    for start, end in sorted(intervals, key=lambda it: it[1]):
        if last_end is None or start >= last_end:
            last_end = end
        else:
            removed += 1
    return removed
