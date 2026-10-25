def bellman_ford(n, edges, source):
    inf = float("inf")
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for a, b, w in edges:
        dist[a][b] = min(dist[a][b], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    for v in range(n):
        if dist[source][v] < inf and dist[v][v] < 0:
            return []
    return [dist[source][v] if dist[source][v] < inf else None for v in range(n)]
