import itertools


def solve(corpus):
    from collections import Counter

    c = Counter()
    for seq in corpus:
        c.update(itertools.pairwise(seq))
    return c.most_common(1)[0]
