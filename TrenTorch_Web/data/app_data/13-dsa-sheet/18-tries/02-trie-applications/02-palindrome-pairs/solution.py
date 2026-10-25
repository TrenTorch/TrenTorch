def palindrome_pairs(words):
    index = {}
    for i, w in enumerate(words):
        index.setdefault(w, []).append(i)
    found = set()
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):
            prefix, suffix = w[:cut], w[cut:]
            if prefix == prefix[::-1]:
                for j in index.get(suffix[::-1], ()):
                    if j != i:
                        found.add((j, i))
            if suffix == suffix[::-1]:
                for j in index.get(prefix[::-1], ()):
                    if j != i:
                        found.add((i, j))
    return [list(pair) for pair in sorted(found)]
