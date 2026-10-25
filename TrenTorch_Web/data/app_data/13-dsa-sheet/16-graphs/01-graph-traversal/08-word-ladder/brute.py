def ladder_length(begin, end, words):
    allowed = set(words)
    if end not in allowed:
        return 0
    nodes = sorted(allowed | {begin})
    inf = float("inf")
    dist = {w: inf for w in nodes}
    dist[begin] = 1
    changed = True
    while changed:
        changed = False
        for a in nodes:
            for b in nodes:
                if dist[a] + 1 < dist[b] and sum(x != y for x, y in zip(a, b)) == 1:
                    dist[b] = dist[a] + 1
                    changed = True
    return dist[end] if dist[end] < inf else 0
