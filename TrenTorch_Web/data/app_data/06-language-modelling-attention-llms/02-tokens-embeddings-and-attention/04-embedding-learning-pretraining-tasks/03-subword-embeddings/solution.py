import numpy as np


def char_ngrams(word, n_min, n_max):
    w = "<" + word + ">"
    grams = [w[i:i + n] for n in range(n_min, n_max + 1) for i in range(len(w) - n + 1)]
    if w not in grams:
        grams.append(w)
    return grams


def subword_embedding(word, table, n_min, n_max, dim):
    vecs = [table[g] for g in char_ngrams(word, n_min, n_max) if g in table]
    if not vecs:
        return np.zeros(dim)
    return np.mean(vecs, axis=0)
