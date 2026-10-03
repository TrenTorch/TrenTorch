import numpy as np


def joint_probability(x, parents, cpts) -> float:
    x = [int(v) for v in x]
    n = len(parents)
    if len(x) != n or len(cpts) != n:
        raise ValueError("x, parents and cpts must have one entry per node")
    prob = 1.0
    for i in range(n):
        table = np.asarray(cpts[i], dtype=float)
        if table.ndim != len(parents[i]) + 1:
            raise ValueError("cpt rank must be the number of parents plus one")
        if not np.allclose(table.sum(axis=-1), 1.0):
            raise ValueError("cpt rows must sum to 1")
        index = tuple(x[p] for p in parents[i]) + (x[i],)
        if any(not 0 <= v < s for v, s in zip(index, table.shape)):
            raise ValueError("value out of range for its table")
        prob *= table[index]
    return float(prob)
