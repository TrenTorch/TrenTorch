def index_pairs(text, words):
    found = set()
    for i in range(len(text)):
        for w in set(words):
            if text.startswith(w, i):
                found.add((i, i + len(w) - 1))
    return [list(p) for p in sorted(found)]
