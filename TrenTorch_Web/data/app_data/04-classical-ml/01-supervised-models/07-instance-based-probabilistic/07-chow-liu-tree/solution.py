import numpy as np


def mutual_information(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a)
    b = np.asarray(b)
    if a.ndim != 1 or a.shape != b.shape:
        raise ValueError("a and b must be 1-D with the same length")
    n = len(a)
    _, ai = np.unique(a, return_inverse=True)
    _, bi = np.unique(b, return_inverse=True)
    joint = np.zeros((ai.max() + 1, bi.max() + 1))
    np.add.at(joint, (ai, bi), 1)
    joint /= n
    pa = joint.sum(axis=1, keepdims=True)
    pb = joint.sum(axis=0, keepdims=True)
    nz = joint > 0
    return float((joint[nz] * np.log2(joint[nz] / (pa @ pb)[nz])).sum())


def chow_liu_tree(X: np.ndarray) -> list[tuple[int, int]]:
    X = np.asarray(X)
    if X.ndim != 2:
        raise ValueError("X must be 2-D")
    d = X.shape[1]
    edges = []
    for i in range(d):
        for j in range(i + 1, d):
            edges.append((mutual_information(X[:, i], X[:, j]), i, j))
    edges.sort(key=lambda e: (-e[0], e[1], e[2]))

    parent = list(range(d))

    def find(u: int) -> int:
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    tree = []
    for _, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            tree.append((i, j))
    return sorted(tree)
