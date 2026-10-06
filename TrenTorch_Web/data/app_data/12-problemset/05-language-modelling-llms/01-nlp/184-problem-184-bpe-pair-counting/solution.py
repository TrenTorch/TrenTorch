import numpy as np

def solve(corpus):
        from collections import Counter
        c=Counter()
        for seq in corpus:
            c.update(zip(seq,seq[1:]))
        return c.most_common(1)[0]
