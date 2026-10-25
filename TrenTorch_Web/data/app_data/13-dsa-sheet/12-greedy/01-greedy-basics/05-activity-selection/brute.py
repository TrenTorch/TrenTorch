def max_activities(starts, ends):
    n = len(starts)
    best = 0
    for mask in range(1 << n):
        chosen = sorted((starts[i], ends[i]) for i in range(n) if mask >> i & 1)
        if all(chosen[k][1] <= chosen[k + 1][0] for k in range(len(chosen) - 1)):
            best = max(best, len(chosen))
    return best
