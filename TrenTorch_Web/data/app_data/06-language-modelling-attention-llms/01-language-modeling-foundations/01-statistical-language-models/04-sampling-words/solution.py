import numpy as np


def sample_word(probs, itos, rng, max_len=50):
    V = len(itos)
    state = 0
    out = []
    while len(out) < max_len:
        cum = np.cumsum(probs[state])
        u = rng.random_sample()
        j = min(int(np.searchsorted(cum, u, side="right")), V - 1)
        if j == 0:
            break
        out.append(itos[j])
        state = j
    return "".join(out)
