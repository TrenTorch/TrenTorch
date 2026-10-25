def find_redundant_connection(edges):
    n = len(edges)

    def is_tree(rest):
        adj = {v: [] for v in range(1, n + 1)}
        for a, b in rest:
            adj[a].append(b)
            adj[b].append(a)
        seen = {1}
        stack = [1]
        while stack:
            node = stack.pop()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return len(seen) == n

    for i in range(len(edges) - 1, -1, -1):
        if is_tree(edges[:i] + edges[i + 1 :]):
            return edges[i]
    return []
