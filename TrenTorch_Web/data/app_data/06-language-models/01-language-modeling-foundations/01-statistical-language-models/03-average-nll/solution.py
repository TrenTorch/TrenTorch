import numpy as np


def average_nll(words, probs, itos):
    stoi = {c: i for i, c in enumerate(itos)}
    rows, cols = [], []
    for word in words:
        seq = ["."] + list(word) + ["."]
        for a, b in zip(seq, seq[1:]):
            rows.append(stoi[a])
            cols.append(stoi[b])
    p = np.asarray(probs, dtype=float)[rows, cols]
    return float(-np.log(p).mean())
