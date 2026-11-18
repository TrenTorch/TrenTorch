def index_pairs(text, words):
    trie = {}
    for word in words:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True
    out = []
    for i in range(len(text)):
        node = trie
        for j in range(i, len(text)):
            node = node.get(text[j])
            if node is None:
                break
            if "$" in node:
                out.append([i, j])
    return out
