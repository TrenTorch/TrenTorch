def shortest_distances(n, edges, source):
    inf = float("inf")
    dist = [inf] * n
    dist[source] = 0
    for _ in range(n):
        for a, b, w in edges:
            if dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
    return [d if d < inf else -1 for d in dist]
