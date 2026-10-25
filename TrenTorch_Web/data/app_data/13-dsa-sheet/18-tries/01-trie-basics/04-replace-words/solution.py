def replace_words(roots, sentence):
    trie = {}
    for root in roots:
        node = trie
        for ch in root:
            node = node.setdefault(ch, {})
        node["$"] = True
    out = []
    for word in sentence.split():
        node = trie
        for i, ch in enumerate(word):
            node = node.get(ch)
            if node is None:
                out.append(word)
                break
            if "$" in node:
                out.append(word[: i + 1])
                break
        else:
            out.append(word)
    return " ".join(out)
