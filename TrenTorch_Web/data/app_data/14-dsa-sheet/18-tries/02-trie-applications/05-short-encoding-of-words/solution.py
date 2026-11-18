def minimum_length_encoding(words):
    trie = {}
    ends = []
    for word in set(words):
        node = trie
        for ch in reversed(word):
            node = node.setdefault(ch, {})
        ends.append((node, len(word)))
    return sum(length + 1 for node, length in ends if not node)
