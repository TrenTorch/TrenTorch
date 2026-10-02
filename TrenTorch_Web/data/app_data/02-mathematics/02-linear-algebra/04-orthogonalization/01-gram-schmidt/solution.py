import numpy as np


def gram_schmidt(vectors):
    basis = []
    for v in vectors:
        w = v.astype(float).copy()
        for u in basis:
            w = w - ((w @ u) / (u @ u)) * u
        basis.append(w / np.linalg.norm(w))
    return basis
