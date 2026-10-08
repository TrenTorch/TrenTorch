import numpy as np


def switch_route(logits):
    logits = np.asarray(logits, dtype=float)
    e = np.exp(logits - logits.max(axis=-1, keepdims=True))
    probs = e / e.sum(axis=-1, keepdims=True)
    idx = probs.argmax(axis=-1)
    gate = probs[np.arange(len(idx)), idx]
    return idx, gate
