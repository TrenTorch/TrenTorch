def tsp(dist):
    n = len(dist)
    if n <= 1:
        return 0
    inf = float("inf")
    full = (1 << n) - 1
    best = [[inf] * n for _ in range(1 << n)]
    best[1][0] = 0
    for mask in range(1, 1 << n):
        if not mask & 1:
            continue
        for last in range(n):
            cost = best[mask][last]
            if cost == inf:
                continue
            for nxt in range(n):
                if not mask >> nxt & 1:
                    new = mask | 1 << nxt
                    value = cost + dist[last][nxt]
                    if value < best[new][nxt]:
                        best[new][nxt] = value
    return min(best[full][last] + dist[last][0] for last in range(1, n))
