from collections import Counter


def top_characters(s, k):
    ranked = sorted(Counter(s).items(), key=lambda kv: (-kv[1], kv[0]))
    return [[ch, n] for ch, n in ranked[:k]]
