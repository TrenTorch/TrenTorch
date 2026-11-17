from collections import deque


def is_bipartite(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    color = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if color[nxt] == -1:
                    color[nxt] = 1 - color[node]
                    queue.append(nxt)
                elif color[nxt] == color[node]:
                    return False
    return True
