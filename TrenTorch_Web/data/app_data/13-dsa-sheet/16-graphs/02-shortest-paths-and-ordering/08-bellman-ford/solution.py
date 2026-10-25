def bellman_ford(n, edges, source):
    inf = float("inf")
    dist = [inf] * n
    dist[source] = 0
    for _ in range(n - 1):
        changed = False
        for a, b, w in edges:
            if dist[a] < inf and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                changed = True
        if not changed:
            break
    for a, b, w in edges:
        if dist[a] < inf and dist[a] + w < dist[b]:
            return []
    return [d if d < inf else None for d in dist]
