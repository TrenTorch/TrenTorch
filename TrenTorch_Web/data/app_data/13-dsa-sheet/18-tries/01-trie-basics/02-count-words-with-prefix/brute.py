def count_with_prefix(words, queries):
    return [sum(1 for w in words if w.startswith(q)) for q in queries]
