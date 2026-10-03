import numpy as np


def solve_analogy(E, vocab, a, b, c):
    idx = {w: i for i, w in enumerate(vocab)}
    E = np.asarray(E, dtype=float)
    target = E[idx[b]] - E[idx[a]] + E[idx[c]]
    norms = np.linalg.norm(E, axis=1)
    tn = np.linalg.norm(target)
    sims = np.zeros(len(vocab))
    ok = (norms > 0) & (tn > 0)
    sims[ok] = (E[ok] @ target) / (norms[ok] * tn)
    for w in (a, b, c):
        sims[idx[w]] = -np.inf
    return vocab[int(np.argmax(sims))]
