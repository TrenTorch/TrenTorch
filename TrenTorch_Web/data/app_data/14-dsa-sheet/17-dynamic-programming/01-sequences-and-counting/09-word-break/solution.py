def word_break(s, words):
    trie = {}
    for word in words:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node[None] = True  # a word ends here
    n = len(s)
    reachable = [True] + [False] * n
    for i in range(n):
        if not reachable[i]:
            continue
        node = trie
        for j in range(i, n):
            node = node.get(s[j])
            if node is None:
                break
            if None in node:
                reachable[j + 1] = True
    return reachable[n]
