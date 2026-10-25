def longest_word(words):
    have = set(words)
    best = ""
    for w in have:
        if all(w[:i] in have for i in range(1, len(w) + 1)):
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
    return best
