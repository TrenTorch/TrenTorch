def job_scheduling(jobs):
    n = len(jobs)
    best = 0
    for mask in range(1 << n):
        chosen = sorted(
            (jobs[i] for i in range(n) if mask >> i & 1), key=lambda j: j[0]
        )
        if all(chosen[k][1] <= chosen[k + 1][0] for k in range(len(chosen) - 1)):
            best = max(best, sum(j[2] for j in chosen))
    return best
