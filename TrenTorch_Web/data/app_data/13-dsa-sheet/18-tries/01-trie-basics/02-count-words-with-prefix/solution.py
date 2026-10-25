def count_with_prefix(words, queries):
    root = {"#": 0}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {"#": 0})
            node["#"] += 1
    out = []
    for q in queries:
        node = root
        for ch in q:
            node = node.get(ch)
            if node is None:
                break
        out.append(node["#"] if node is not None else 0)
    return out
