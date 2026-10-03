import numpy as np


def bigram_counts(words):
    itos = ["."] + sorted(set("".join(words)))
    stoi = {c: i for i, c in enumerate(itos)}
    counts = np.zeros((len(itos), len(itos)), dtype=np.int64)
    for word in words:
        seq = ["."] + list(word) + ["."]
        for a, b in zip(seq, seq[1:]):
            counts[stoi[a], stoi[b]] += 1
    return counts, itos
