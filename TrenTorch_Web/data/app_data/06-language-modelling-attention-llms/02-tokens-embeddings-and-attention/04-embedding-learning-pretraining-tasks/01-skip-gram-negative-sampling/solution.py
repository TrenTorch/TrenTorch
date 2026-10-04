import numpy as np


def skipgram_pairs(token_ids, window):
    pairs = []
    n = len(token_ids)
    for i in range(n):
        for j in range(max(0, i - window), min(n, i + window + 1)):
            if j != i:
                pairs.append((token_ids[i], token_ids[j]))
    return pairs


def sgns_loss(W_in, W_out, center, context, negatives):
    v = W_in[np.asarray(center)]
    pos = (W_out[np.asarray(context)] * v).sum(axis=-1)
    neg = np.einsum("bkd,bd->bk", W_out[np.asarray(negatives)], v)
    return float((np.logaddexp(0.0, -pos) + np.logaddexp(0.0, neg).sum(axis=1)).mean())
