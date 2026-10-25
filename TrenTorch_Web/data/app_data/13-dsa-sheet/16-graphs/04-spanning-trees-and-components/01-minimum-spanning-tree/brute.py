def mst_weight(n, edges):
    inf = float("inf")
    best = [[inf] * n for _ in range(n)]
    for a, b, w in edges:
        best[a][b] = min(best[a][b], w)
        best[b][a] = min(best[b][a], w)
    in_tree = [False] * n
    key = [inf] * n
    key[0] = 0
    total = 0
    for _ in range(n):
        u = min((v for v in range(n) if not in_tree[v]), key=lambda v: key[v])
        if key[u] == inf:
            return -1
        in_tree[u] = True
        total += key[u]
        for v in range(n):
            if not in_tree[v] and best[u][v] < key[v]:
                key[v] = best[u][v]
    return total
