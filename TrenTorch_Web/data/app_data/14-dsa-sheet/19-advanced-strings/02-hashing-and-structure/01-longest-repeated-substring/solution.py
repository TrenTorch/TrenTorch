def longest_repeated_length(s):
    nxt = [{}]
    link = [-1]
    length = [0]
    occ = [0]
    last = 0
    for ch in s:
        cur = len(nxt)
        nxt.append({})
        link.append(0)
        length.append(length[last] + 1)
        occ.append(1)
        p = last
        while p != -1 and ch not in nxt[p]:
            nxt[p][ch] = cur
            p = link[p]
        if p != -1:
            q = nxt[p][ch]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = len(nxt)
                nxt.append(dict(nxt[q]))
                link.append(link[q])
                length.append(length[p] + 1)
                occ.append(0)
                while p != -1 and nxt[p].get(ch) == q:
                    nxt[p][ch] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur

    by_length = [[] for _ in range(len(s) + 1)]
    for v in range(1, len(nxt)):
        by_length[length[v]].append(v)
    best = 0
    for size in range(len(s), 0, -1):
        for v in by_length[size]:
            if occ[v] >= 2:
                best = max(best, size)
            occ[link[v]] += occ[v]
    return best
