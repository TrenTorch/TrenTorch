import numpy as np


def make_pairs(docs, rng):
    if len(docs) < 2:
        raise ValueError("need at least two documents for negatives")
    out = []
    for i, doc in enumerate(docs):
        others = [s for j, d in enumerate(docs) if j != i for s in d]
        for k in range(len(doc) - 1):
            if rng.random_sample() < 0.5:
                out.append((doc[k], doc[k + 1], 1))
            else:
                out.append((doc[k], others[rng.randint(len(others))], 0))
    return out
