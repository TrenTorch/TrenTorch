def has_cycle_directed(n, edges):
    reach = [[False] * n for _ in range(n)]
    for a, b in edges:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return any(reach[i][i] for i in range(n))
