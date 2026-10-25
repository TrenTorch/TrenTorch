from bisect import bisect_right


def job_scheduling(jobs):
    items = sorted(jobs, key=lambda j: j[1])
    ends = [j[1] for j in items]
    best = [0] * (len(items) + 1)
    for i, (start, end, profit) in enumerate(items, 1):
        before = bisect_right(ends, start, 0, i - 1)
        best[i] = max(best[i - 1], profit + best[before])
    return best[len(items)]
