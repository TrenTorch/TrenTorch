from collections import Counter

def solve(tokens, k):
    """Return the k most frequent tokens as (token, count) pairs."""
    if k < 0:
        raise ValueError("k must be non-negative")
    counts = Counter(tokens)
    order = {token: index for index, token in enumerate(dict.fromkeys(tokens))}
    return sorted(counts.items(), key=lambda item: (-item[1], order[item[0]]))[:k]
