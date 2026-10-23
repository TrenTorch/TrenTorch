def valid_tree(n, edges):
    if n == 0:
        return False
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {0}
    stack = [0]
    while stack:
        node = stack.pop()
        for nxt in adj[node]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    has_cycle = False
    counted = set()
    for i, (a, b) in enumerate(edges):
        if a == b or (min(a, b), max(a, b)) in counted:
            has_cycle = True
        counted.add((min(a, b), max(a, b)))
    return len(seen) == n and len(edges) == n - 1 and not has_cycle
