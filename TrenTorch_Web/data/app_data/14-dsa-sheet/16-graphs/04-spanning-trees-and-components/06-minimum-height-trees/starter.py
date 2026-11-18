def min_height_trees(n: int, edges: list[list[int]]) -> list[int]:
    """Return the roots that give a tree of the smallest height."""
    # This is correct but too slow: it measures the height of the tree from every node as the root.
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    heights = []
    for root in range(n):
        depth = {root: 0}
        queue = [root]
        for node in queue:
            for nxt in adj[node]:
                if nxt not in depth:
                    depth[nxt] = depth[node] + 1
                    queue.append(nxt)
        heights.append(max(depth.values()))
    best = min(heights)
    return [v for v in range(n) if heights[v] == best]
