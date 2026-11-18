from collections import deque


def stream_checker(words, stream):
    goto = [{}]
    fail = [0]
    ends = [False]
    for word in words:
        node = 0
        for ch in word:
            child = goto[node].get(ch)
            if child is None:
                goto.append({})
                fail.append(0)
                ends.append(False)
                child = len(goto) - 1
                goto[node][ch] = child
            node = child
        ends[node] = True
    queue = deque(goto[0].values())
    while queue:
        node = queue.popleft()
        if ends[fail[node]]:
            ends[node] = True
        for ch, child in goto[node].items():
            f = fail[node]
            while f and ch not in goto[f]:
                f = fail[f]
            fail[child] = goto[f].get(ch, 0)
            queue.append(child)

    out = []
    state = 0
    for ch in stream:
        while state and ch not in goto[state]:
            state = fail[state]
        state = goto[state].get(ch, 0)
        out.append(ends[state])
    return out
