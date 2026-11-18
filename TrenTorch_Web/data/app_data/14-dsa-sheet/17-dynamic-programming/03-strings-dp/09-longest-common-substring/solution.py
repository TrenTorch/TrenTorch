def longest_common_substring(a, b):
    # suffix automaton of a
    nxt = [{}]
    link = [-1]
    length = [0]
    last = 0
    for ch in a:
        cur = len(nxt)
        nxt.append({})
        length.append(length[last] + 1)
        link.append(0)
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
                length.append(length[p] + 1)
                link.append(link[q])
                while p != -1 and nxt[p].get(ch) == q:
                    nxt[p][ch] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur

    best = match = state = 0
    for ch in b:
        while state and ch not in nxt[state]:
            state = link[state]
            match = length[state]
        if ch in nxt[state]:
            state = nxt[state][ch]
            match += 1
        else:
            state = match = 0
        best = max(best, match)
    return best
