def articulation_points(n, edges):
    def components(skip):
        adj = [[] for _ in range(n)]
        for a, b in edges:
            if a != skip and b != skip:
                adj[a].append(b)
                adj[b].append(a)
        seen = [False] * n
        count = 0
        for s in range(n):
            if s != skip and not seen[s]:
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
    return [v for v in range(n) if components(v) > base]
