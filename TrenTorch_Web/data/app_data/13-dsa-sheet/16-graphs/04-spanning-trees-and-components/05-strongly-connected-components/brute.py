def count_scc(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for a, b in edges:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    groups = {
        tuple(j for j in range(n) if reach[i][j] and reach[j][i]) for i in range(n)
    }
    return len(groups)
