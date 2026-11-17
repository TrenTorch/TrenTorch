def longest_word(words):
    by_length = {}
    for word in set(words):
        by_length.setdefault(len(word), []).append(word)
    built = {""}
    best = ""
    length = 1
    while True:
        good = [w for w in by_length.get(length, ()) if w[:-1] in built]
        if not good:
            return best
        built.update(good)
        best = min(good)
        length += 1
