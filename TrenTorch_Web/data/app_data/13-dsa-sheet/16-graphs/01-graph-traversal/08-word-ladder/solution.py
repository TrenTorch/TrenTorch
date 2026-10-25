from collections import deque


def ladder_length(begin, end, words):
    allowed = set(words)
    if end not in allowed:
        return 0
    groups = {}
    for word in allowed | {begin}:
        for i in range(len(word)):
            groups.setdefault(word[:i] + "*" + word[i + 1 :], []).append(word)
    seen = {begin}
    queue = deque([(begin, 1)])
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            for other in groups.get(word[:i] + "*" + word[i + 1 :], ()):
                if other not in seen:
                    seen.add(other)
                    queue.append((other, steps + 1))
    return 0
