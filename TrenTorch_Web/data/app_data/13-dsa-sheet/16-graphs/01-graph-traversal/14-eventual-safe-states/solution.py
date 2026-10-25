from collections import deque


def eventual_safe_nodes(n, edges):
    rev = [[] for _ in range(n)]
    out_degree = [0] * n
    for a, b in edges:
        rev[b].append(a)
        out_degree[a] += 1
    queue = deque(v for v in range(n) if out_degree[v] == 0)
    safe = [False] * n
    while queue:
        node = queue.popleft()
        safe[node] = True
        for p in rev[node]:
            out_degree[p] -= 1
            if out_degree[p] == 0:
                queue.append(p)
    return [v for v in range(n) if safe[v]]
