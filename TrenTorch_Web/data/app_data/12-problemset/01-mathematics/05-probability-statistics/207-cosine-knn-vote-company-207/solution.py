import numpy as np

def solve(X, y, q):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    q = np.asarray(q, dtype=float)
    den = np.linalg.norm(X, axis=1) * np.linalg.norm(q)
    scores = np.divide(X @ q, den, out=np.zeros(len(X)), where=den != 0)
    return y[int(np.argmax(scores))]
