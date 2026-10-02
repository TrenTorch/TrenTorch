import numpy as np

from _load import load_solution

householder_vector = load_solution("math-householder-reflections").householder_vector
apply_householder = load_solution("math-householder-reflections").apply_householder


def householder_qr(a):
    r = np.array(a, dtype=float)
    m, n = r.shape
    q = np.eye(m)
    for k in range(min(m - 1, n)):
        v = householder_vector(r[k:, k])
        if not np.any(v):
            continue
        r[k:, :] = apply_householder(v, r[k:, :])
        q[:, k:] = apply_householder(v, q[:, k:].T).T
    return q, np.triu(r)


def back_substitution(r, y):
    r = np.asarray(r, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - r[i, i + 1 :] @ x[i + 1 :]) / r[i, i]
    return x


def least_squares_qr(a, b):
    a = np.asarray(a, dtype=float)
    n = a.shape[1]
    q, r = householder_qr(a)
    c = q.T @ np.asarray(b, dtype=float)
    return back_substitution(r[:n, :n], c[:n])
