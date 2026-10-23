def articulation_points(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    disc = [-1] * n
    low = [0] * n
    cut = set()
    timer = 0
    for root in range(n):
        if disc[root] != -1:
            continue
        disc[root] = low[root] = timer
        timer += 1
        root_children = 0
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
                    if node == root:
                        root_children += 1
                    stack.append((nxt, node, 0))
                else:
                    low[node] = min(low[node], disc[nxt])
            elif parent != -1:
                low[parent] = min(low[parent], low[node])
                if parent != root and low[node] >= disc[parent]:
                    cut.add(parent)
        if root_children >= 2:
            cut.add(root)
    return sorted(cut)
