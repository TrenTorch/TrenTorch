def run_union_find(n, ops):
    adj = [[] for _ in range(n)]

    def component(start):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    out = []
    for op in ops:
        parts = op.split()
        if parts[0] == "union":
            a, b = int(parts[1]), int(parts[2])
            adj[a].append(b)
            adj[b].append(a)
        elif parts[0] == "connected":
            out.append(1 if int(parts[2]) in component(int(parts[1])) else 0)
        else:
            out.append(len(component(int(parts[1]))))
    return out
