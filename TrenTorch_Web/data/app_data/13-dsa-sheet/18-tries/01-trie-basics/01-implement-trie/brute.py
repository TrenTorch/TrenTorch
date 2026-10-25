def run_trie(ops):
    words = set()
    out = []
    for op in ops:
        kind, word = op.split()
        if kind == "insert":
            words.add(word)
        elif kind == "search":
            out.append(word in words)
        else:
            out.append(any(w.startswith(word) for w in words))
    return out
