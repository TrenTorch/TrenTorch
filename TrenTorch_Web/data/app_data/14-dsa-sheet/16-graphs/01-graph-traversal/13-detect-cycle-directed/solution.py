def has_cycle_directed(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
    state = [0] * n
    for start in range(n):
        if state[start]:
            continue
        state[start] = 1
        stack = [(start, 0)]
        while stack:
            node, i = stack.pop()
            if i < len(adj[node]):
                stack.append((node, i + 1))
                nxt = adj[node][i]
                if state[nxt] == 1:
                    return True
                if state[nxt] == 0:
                    state[nxt] = 1
                    stack.append((nxt, 0))
            else:
                state[node] = 2
    return False
