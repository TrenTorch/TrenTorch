def index_pairs(text: str, words: list[str]) -> list[list[int]]:
    """Return all [start, end] pairs where text[start:end + 1] is one of the words."""
    # This is correct but too slow: it checks every word at every position.
    out = []
    for i in range(len(text)):
        for w in words:
            if text.startswith(w, i):
                out.append([i, i + len(w) - 1])
    return sorted(set(map(tuple, out)))
