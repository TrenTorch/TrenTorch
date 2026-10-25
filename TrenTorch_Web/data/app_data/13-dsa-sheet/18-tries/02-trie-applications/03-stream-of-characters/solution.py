def stream_checker(words, stream):
    trie = {}
    for word in words:
        node = trie
        for ch in reversed(word):
            node = node.setdefault(ch, {})
        node["$"] = True
    maxlen = max((len(w) for w in words), default=0)
    out = []
    for i in range(len(stream)):
        node = trie
        hit = False
        for k in range(i, max(-1, i - maxlen), -1):
            node = node.get(stream[k])
            if node is None:
                break
            if "$" in node:
                hit = True
                break
        out.append(hit)
    return out
