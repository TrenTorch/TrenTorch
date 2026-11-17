def can_color_graph(n, edges, colors):
    if any(u == v for u, v in edges):
        return False
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * n

    def go(i):
        if i == n:
            return True
        for c in range(colors):
            if all(color[j] != c for j in adj[i]):
                color[i] = c
                if go(i + 1):
                    return True
                color[i] = -1
        return False

    return go(0)
