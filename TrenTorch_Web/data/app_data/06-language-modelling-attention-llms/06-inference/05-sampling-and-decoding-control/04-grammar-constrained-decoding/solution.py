import numpy as np


def advance(transitions, state, token):
    for ch in token:
        state = transitions.get((state, ch))
        if state is None:
            return None
    return state


def allowed_token_ids(transitions, state, vocab):
    return [i for i, tok in enumerate(vocab) if tok and advance(transitions, state, tok) is not None]


def mask_logits(logits, allowed):
    out = np.full(len(logits), -np.inf)
    idx = list(allowed)
    out[idx] = np.asarray(logits, dtype=float)[idx]
    return out
