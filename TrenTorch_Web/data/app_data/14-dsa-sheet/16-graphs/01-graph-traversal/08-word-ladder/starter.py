def ladder_length(begin: str, end: str, words: list[str]) -> int:
    """Return the length of the shortest word chain from begin to end."""
    # This is correct but too slow: it compares each word with every other word to find the neighbours.
    allowed = set(words)
    if end not in allowed:
        return 0
    frontier = [begin]
    seen = {begin}
    steps = 1
    while frontier:
        nxt = []
        for word in frontier:
            if word == end:
                return steps
            for other in allowed:
                if other not in seen and sum(a != b for a, b in zip(word, other)) == 1:
                    seen.add(other)
                    nxt.append(other)
        frontier = nxt
        steps += 1
    return 0
