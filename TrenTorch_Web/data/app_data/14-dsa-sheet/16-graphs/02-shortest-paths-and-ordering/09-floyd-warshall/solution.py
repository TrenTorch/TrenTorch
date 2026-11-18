def all_pairs_shortest(n, edges):
    inf = float("inf")
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for a, b, w in edges:
        if w < dist[a][b]:
            dist[a][b] = w
    for k in range(n):
        row_k = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == inf:
                continue
            row_i = dist[i]
            for j in range(n):
                if dik + row_k[j] < row_i[j]:
                    row_i[j] = dik + row_k[j]
    return [[x if x < inf else -1 for x in row] for row in dist]
