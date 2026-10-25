def count_scc(n, edges):
    adj = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        rev[b].append(a)
    seen = [False] * n
    order = []
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            node, i = stack.pop()
            if i < len(adj[node]):
                stack.append((node, i + 1))
                nxt = adj[node][i]
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, 0))
            else:
                order.append(node)
    seen = [False] * n
    count = 0
    for start in reversed(order):
        if seen[start]:
            continue
        count += 1
        seen[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in rev[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return count
