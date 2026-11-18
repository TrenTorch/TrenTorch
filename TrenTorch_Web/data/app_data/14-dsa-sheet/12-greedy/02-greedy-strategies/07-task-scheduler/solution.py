def least_interval(tasks, n):
    if not tasks:
        return 0
    counts = {}
    for t in tasks:
        counts[t] = counts.get(t, 0) + 1
    m = max(counts.values())
    ties = sum(1 for c in counts.values() if c == m)
    return max(len(tasks), (m - 1) * (n + 1) + ties)
