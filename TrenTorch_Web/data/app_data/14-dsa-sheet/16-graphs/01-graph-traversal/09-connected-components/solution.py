def count_components(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * n
    count = 0
    for start in range(n):
        if seen[start]:
            continue
        count += 1
        seen[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in adj[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return count
