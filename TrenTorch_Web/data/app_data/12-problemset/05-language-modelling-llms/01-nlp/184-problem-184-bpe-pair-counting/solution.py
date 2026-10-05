import numpy as np

def solve(corpus):
    """Return the most frequent adjacent token pair and its count across corpus sequences."""
    from collections import Counter
    c=Counter()
    for seq in corpus:
        c.update(zip(seq,seq[1:]))
    return c.most_common(1)[0]
