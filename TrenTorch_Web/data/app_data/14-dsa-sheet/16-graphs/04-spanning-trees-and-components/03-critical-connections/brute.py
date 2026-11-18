def critical_connections(n, connections):
    def components(skip):
        adj = [[] for _ in range(n)]
        for i, (a, b) in enumerate(connections):
            if i != skip:
                adj[a].append(b)
                adj[b].append(a)
        seen = [False] * n
        count = 0
        for s in range(n):
            if not seen[s]:
                count += 1
                seen[s] = True
                stack = [s]
                while stack:
                    u = stack.pop()
                    for v in adj[u]:
                        if not seen[v]:
                            seen[v] = True
                            stack.append(v)
        return count

    base = components(-1)
    return sorted(
        [min(a, b), max(a, b)]
        for i, (a, b) in enumerate(connections)
        if components(i) > base
    )
