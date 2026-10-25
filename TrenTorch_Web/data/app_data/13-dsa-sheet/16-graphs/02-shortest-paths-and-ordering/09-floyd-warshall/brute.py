import heapq


def all_pairs_shortest(n, edges):
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    out = []
    for source in range(n):
        inf = float("inf")
        dist = [inf] * n
        dist[source] = 0
        heap = [(0, source)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(heap, (dist[v], v))
        out.append([x if x < inf else -1 for x in dist])
    return out
