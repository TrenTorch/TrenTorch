def max_activities(starts, ends):
    count = 0
    last_end = -1
    for end, start in sorted(zip(ends, starts)):
        if start >= last_end:
            count += 1
            last_end = end
    return count
