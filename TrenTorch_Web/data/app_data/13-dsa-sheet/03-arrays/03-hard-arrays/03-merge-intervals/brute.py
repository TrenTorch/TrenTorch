def merge_intervals(intervals):
    covered = set()
    for start, end in intervals:
        covered.update(range(2 * start, 2 * end + 1))
    out = []
    for point in sorted(covered):
        if out and point == out[-1][1] + 1:
            out[-1][1] = point
        else:
            out.append([point, point])
    return [[a // 2, b // 2] for a, b in out]
