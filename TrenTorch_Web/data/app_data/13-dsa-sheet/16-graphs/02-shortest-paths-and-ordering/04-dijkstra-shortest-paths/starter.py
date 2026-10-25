def shortest_distances(n: int, edges: list[list[int]], source: int) -> list[int]:
    """Return the shortest distance from source to every node, or -1."""
    # This is correct but too slow: it picks the closest unfinished node by scanning all nodes each time.
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    inf = float("inf")
    dist = [inf] * n
    dist[source] = 0
    done = [False] * n
    for _ in range(n):
        best = -1
        for v in range(n):
            if not done[v] and dist[v] < inf and (best == -1 or dist[v] < dist[best]):
                best = v
        if best == -1:
            break
        done[best] = True
        for nxt, w in adj[best]:
            if dist[best] + w < dist[nxt]:
                dist[nxt] = dist[best] + w
    return [d if d < inf else -1 for d in dist]
