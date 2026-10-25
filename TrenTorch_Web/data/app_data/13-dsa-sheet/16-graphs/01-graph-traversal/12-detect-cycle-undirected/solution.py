def has_cycle_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        if a == b:
            return True
        adj[a].append((b, i))
        adj[b].append((a, i))
    seen = [False] * n
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, -1)]
        while stack:
            node, via = stack.pop()
            for nxt, edge_id in adj[node]:
                if edge_id == via:
                    continue
                if seen[nxt]:
                    return True
                seen[nxt] = True
                stack.append((nxt, edge_id))
    return False
