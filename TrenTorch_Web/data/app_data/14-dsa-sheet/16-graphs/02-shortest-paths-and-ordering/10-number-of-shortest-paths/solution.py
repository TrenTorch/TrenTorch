import heapq


def count_shortest_paths(n, roads):
    mod = 10**9 + 7
    adj = [[] for _ in range(n)]
    for a, b, t in roads:
        adj[a].append((b, t))
        adj[b].append((a, t))
    inf = float("inf")
    dist = [inf] * n
    ways = [0] * n
    dist[0] = 0
    ways[0] = 1
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, t in adj[u]:
            nd = d + t
            if nd < dist[v]:
                dist[v] = nd
                ways[v] = ways[u]
                heapq.heappush(heap, (nd, v))
            elif nd == dist[v]:
                ways[v] = (ways[v] + ways[u]) % mod
    return ways[n - 1] % mod
