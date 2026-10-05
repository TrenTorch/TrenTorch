import numpy as np
from collections import Counter


def _ngrams(tokens, n):
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def modified_precision(candidate, references, n):
    cand = _ngrams(candidate, n)
    total = sum(cand.values())
    if total == 0:
        return 0.0
    max_ref = Counter()
    for ref in references:
        for gram, c in _ngrams(ref, n).items():
            max_ref[gram] = max(max_ref[gram], c)
    clipped = sum(min(c, max_ref[g]) for g, c in cand.items())
    return clipped / total


def bleu(candidate, references, max_n=4):
    precisions = [modified_precision(candidate, references, n) for n in range(1, max_n + 1)]
    if min(precisions) == 0.0:
        return 0.0
    c = len(candidate)
    r = min((len(ref) for ref in references), key=lambda l: (abs(l - c), l))
    bp = 1.0 if c > r else float(np.exp(1 - r / c))
    return float(bp * np.exp(np.mean(np.log(precisions))))
