def max_job_profit(jobs):
    n = len(jobs)
    best = 0
    for mask in range(1 << n):
        chosen = sorted((jobs[i] for i in range(n) if mask >> i & 1))
        if all(k + 1 <= d for k, (d, _) in enumerate(chosen)):
            best = max(best, sum(p for _, p in chosen))
    return best
