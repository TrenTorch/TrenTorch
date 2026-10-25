def job_scheduling(jobs: list[list[int]]) -> int:
    """Return the largest profit from jobs that do not overlap."""
    # This is correct but too slow: for every job it scans all the earlier jobs.
    items = sorted(jobs, key=lambda j: j[1])
    best = [0] * (len(items) + 1)
    for i, (start, end, profit) in enumerate(items, 1):
        take = profit
        for k in range(i - 1, 0, -1):
            if items[k - 1][1] <= start:
                take += best[k]
                break
        best[i] = max(best[i - 1], take)
    return best[len(items)]
