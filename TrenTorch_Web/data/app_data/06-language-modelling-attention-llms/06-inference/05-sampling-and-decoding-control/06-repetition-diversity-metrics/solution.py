def _grams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def distinct_n(tokens, n):
    grams = _grams(tokens, n)
    return len(set(grams)) / len(grams) if grams else 0.0


def corpus_distinct_n(samples, n):
    grams = [g for s in samples for g in _grams(s, n)]
    return len(set(grams)) / len(grams) if grams else 0.0
