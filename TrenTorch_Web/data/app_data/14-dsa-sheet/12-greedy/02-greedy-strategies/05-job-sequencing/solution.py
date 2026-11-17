def max_job_profit(jobs):
    limit = min(max((d for d, _ in jobs), default=0), len(jobs))
    parent = list(range(limit + 1))

    def find(t):
        while parent[t] != t:
            parent[t] = parent[parent[t]]
            t = parent[t]
        return t

    total = 0
    for deadline, profit in sorted(jobs, key=lambda j: -j[1]):
        slot = find(min(deadline, limit))
        if slot > 0:
            parent[slot] = slot - 1
            total += profit
    return total
