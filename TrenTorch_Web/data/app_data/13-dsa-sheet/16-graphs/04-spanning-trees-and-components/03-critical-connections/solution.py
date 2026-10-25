def critical_connections(n, connections):
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)
    disc = [-1] * n
    low = [0] * n
    bridges = []
    timer = 0
    for root in range(n):
        if disc[root] != -1:
            continue
        disc[root] = low[root] = timer
        timer += 1
        stack = [(root, -1, 0)]
        while stack:
            node, parent, i = stack.pop()
            if i < len(adj[node]):
                stack.append((node, parent, i + 1))
                nxt = adj[node][i]
                if nxt == parent:
                    continue
                if disc[nxt] == -1:
                    disc[nxt] = low[nxt] = timer
                    timer += 1
                    stack.append((nxt, node, 0))
                else:
                    low[node] = min(low[node], disc[nxt])
            elif parent != -1:
                low[parent] = min(low[parent], low[node])
                if low[node] > disc[parent]:
                    bridges.append([min(parent, node), max(parent, node)])
    return sorted(bridges)
