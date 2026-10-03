from collections import Counter, defaultdict

import numpy as np


def trigram_next_distribution(sentences, w1, w2, alpha=1.0):
    vocab = sorted({t for s in sentences for t in s} | {"</s>"})
    follows = defaultdict(Counter)
    for s in sentences:
        seq = ["<s>", "<s>"] + list(s) + ["</s>"]
        for a, b, c in zip(seq, seq[1:], seq[2:]):
            follows[(a, b)][c] += 1
    counts = np.array([follows[(w1, w2)][t] for t in vocab], dtype=float)
    probs = (counts + alpha) / (counts.sum() + alpha * len(vocab))
    return vocab, probs
