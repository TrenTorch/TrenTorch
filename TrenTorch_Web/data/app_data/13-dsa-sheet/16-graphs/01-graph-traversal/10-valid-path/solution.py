def valid_path(n, edges, source, destination):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * n
    seen[source] = True
    stack = [source]
    while stack:
        node = stack.pop()
        if node == destination:
            return True
        for nxt in adj[node]:
            if not seen[nxt]:
                seen[nxt] = True
                stack.append(nxt)
    return False
