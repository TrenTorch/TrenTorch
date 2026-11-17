def min_height_trees(n, edges):
    if n <= 2:
        return list(range(n))
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    degree = [len(a) for a in adj]
    leaves = [v for v in range(n) if degree[v] == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        nxt = []
        for leaf in leaves:
            for other in adj[leaf]:
                degree[other] -= 1
                if degree[other] == 1:
                    nxt.append(other)
        leaves = nxt
    return sorted(leaves)
