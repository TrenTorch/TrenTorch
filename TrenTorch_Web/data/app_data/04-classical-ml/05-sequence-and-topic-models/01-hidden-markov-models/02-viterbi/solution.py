import numpy as np


def _check_hmm(pi, A, B):
    pi = np.asarray(pi, dtype=float)
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    K = pi.shape[0] if pi.ndim == 1 else -1
    if pi.ndim != 1 or A.shape != (K, K) or B.ndim != 2 or B.shape[0] != K:
        raise ValueError("pi, A, and B have inconsistent shapes")
    if np.any(pi < 0) or np.any(A < 0) or np.any(B < 0):
        raise ValueError("probabilities must be nonnegative")
    if not np.isclose(pi.sum(), 1.0) or not np.allclose(A.sum(axis=1), 1.0) or not np.allclose(B.sum(axis=1), 1.0):
        raise ValueError("pi must sum to 1 and each row of A and B must sum to 1")
    return pi, A, B


def viterbi(pi: np.ndarray, A: np.ndarray, B: np.ndarray, obs):
    pi, A, B = _check_hmm(pi, A, B)
    obs = np.asarray(obs, dtype=int)
    if obs.ndim != 1 or obs.size == 0:
        raise ValueError("obs must be a nonempty 1-D sequence")
    if np.any((obs < 0) | (obs >= B.shape[1])):
        raise ValueError("observations out of range")
    T, K = obs.size, pi.size
    delta = pi * B[:, obs[0]]
    backptr = np.zeros((T, K), dtype=int)
    for t in range(1, T):
        candidates = delta[:, None] * A
        backptr[t] = candidates.argmax(axis=0)
        delta = candidates.max(axis=0) * B[:, obs[t]]
    state = int(delta.argmax())
    prob = float(delta[state])
    path = [state]
    for t in range(T - 1, 0, -1):
        state = int(backptr[t, state])
        path.append(state)
    path.reverse()
    return path, prob
