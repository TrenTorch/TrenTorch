def min_cost_connect_points(points):
    n = len(points)
    if n == 0:
        return 0
    inf = float("inf")
    best = [inf] * n
    best[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            if not used[v] and (u == -1 or best[v] < best[u]):
                u = v
        used[u] = True
        total += best[u]
        ux, uy = points[u]
        for v in range(n):
            if not used[v]:
                dist = abs(points[v][0] - ux) + abs(points[v][1] - uy)
                if dist < best[v]:
                    best[v] = dist
    return total
