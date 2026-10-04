import numpy as np
from collections import Counter

def solve(corpus):
    """Implement bpe pair counting according to the contract."""
    from collections import Counter
    c = Counter()
    for seq in corpus:
        c.update(zip(seq, seq[1:]))
    return c.most_common(1)[0]
