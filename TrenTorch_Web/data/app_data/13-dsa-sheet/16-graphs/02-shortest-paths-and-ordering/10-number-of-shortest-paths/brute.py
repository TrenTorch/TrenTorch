def count_shortest_paths(n, roads):
    adj = [[] for _ in range(n)]
    for a, b, t in roads:
        adj[a].append((b, t))
        adj[b].append((a, t))
    found = []

    def walk(node, seen, total):
        if node == n - 1:
            found.append(total)
            return
        for nxt, t in adj[node]:
            if nxt not in seen:
                walk(nxt, seen | {nxt}, total + t)

    walk(0, {0}, 0)
    if not found:
        return 0
    return found.count(min(found)) % (10**9 + 7)
