import heapq


def alien_order(words):
    letters = sorted({ch for w in words for ch in w})
    edges = set()
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                edges.add((x, y))
                break
        else:
            if len(a) > len(b):
                return ""
    adj = {ch: [] for ch in letters}
    in_degree = {ch: 0 for ch in letters}
    for x, y in edges:
        adj[x].append(y)
        in_degree[y] += 1
    heap = [ch for ch in letters if in_degree[ch] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        ch = heapq.heappop(heap)
        out.append(ch)
        for nxt in adj[ch]:
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                heapq.heappush(heap, nxt)
    return "".join(out) if len(out) == len(letters) else ""
