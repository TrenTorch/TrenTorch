import numpy as np


def mask_tokens(ids, mask_id, vocab_size, special_ids, rng, mask_prob=0.15):
    ids = np.asarray(ids)
    u = rng.random_sample(len(ids))
    chosen = (u < mask_prob) & ~np.isin(ids, list(special_ids))
    k = int(chosen.sum())
    r = rng.random_sample(k)
    rand_tokens = rng.randint(0, vocab_size, size=k)
    inputs = ids.copy()
    labels = np.full(ids.shape, -100, dtype=ids.dtype)
    labels[chosen] = ids[chosen]
    pos = np.where(chosen)[0]
    inputs[pos[r < 0.8]] = mask_id
    swap = (r >= 0.8) & (r < 0.9)
    inputs[pos[swap]] = rand_tokens[swap]
    return inputs, labels
