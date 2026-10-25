def eventual_safe_nodes(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
    reach = [[False] * n for _ in range(n)]
    for a, b in edges:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    bad = [
        any(reach[v][u] and reach[u][u] for u in range(n)) or reach[v][v]
        for v in range(n)
    ]
    return [v for v in range(n) if not bad[v]]
