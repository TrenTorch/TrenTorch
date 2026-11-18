def run_trie(ops):
    root = {}

    def walk(word):
        node = root
        for ch in word:
            node = node.get(ch)
            if node is None:
                return None
        return node

    out = []
    for op in ops:
        kind, word = op.split()
        if kind == "insert":
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = True
        elif kind == "search":
            node = walk(word)
            out.append(node is not None and "$" in node)
        else:
            out.append(walk(word) is not None)
    return out
