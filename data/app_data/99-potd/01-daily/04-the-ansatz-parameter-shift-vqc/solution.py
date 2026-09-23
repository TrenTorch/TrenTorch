import numpy as np


def _apply_ry(state: np.ndarray, qubit: int, theta: float) -> np.ndarray:
    c, s = np.cos(theta / 2.0), np.sin(theta / 2.0)
    moved = np.moveaxis(state, qubit, 0)
    a0, a1 = moved[0], moved[1]
    new0 = c * a0 - s * a1
    new1 = s * a0 + c * a1
    new_moved = np.stack([new0, new1], axis=0)
    return np.moveaxis(new_moved, 0, qubit)


def _apply_cnot(state: np.ndarray, control: int, target: int) -> np.ndarray:
    moved = np.moveaxis(state, [control, target], [0, 1])
    new_moved = moved.copy()
    new_moved[1, 0] = moved[1, 1]
    new_moved[1, 1] = moved[1, 0]
    return np.moveaxis(new_moved, [0, 1], [control, target])


def circuit_output(x: np.ndarray, theta: np.ndarray, n: int, L: int) -> float:
    state = np.zeros((2,) * n)
    state[(0,) * n] = 1.0

    for i in range(n):
        state = _apply_ry(state, i, x[i])

    for l in range(L):
        for i in range(n - 1):
            state = _apply_cnot(state, i, i + 1)
        for i in range(n):
            state = _apply_ry(state, i, theta[l, i])

    probs = state ** 2
    p0 = probs[0, ...].sum()
    p1 = probs[1, ...].sum()
    return float(p0 - p1)


def train_and_predict(
    X: np.ndarray,
    y: np.ndarray,
    n: int,
    L: int,
    theta_init: np.ndarray,
    eta: float,
    T: int,
    queries: np.ndarray,
) -> np.ndarray:
    theta = np.array(theta_init, dtype=float).reshape(L, n).copy()
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n_train = X.shape[0]

    for _ in range(T):
        preds = np.array([circuit_output(X[k], theta, n, L) for k in range(n_train)])
        residual = preds - y

        grad = np.zeros((L, n))
        for l in range(L):
            for i in range(n):
                shift = np.zeros((L, n))
                shift[l, i] = np.pi / 2
                plus = np.array([circuit_output(X[k], theta + shift, n, L) for k in range(n_train)])
                minus = np.array([circuit_output(X[k], theta - shift, n, L) for k in range(n_train)])
                dp_dtheta = (plus - minus) / 2.0
                grad[l, i] = (2.0 / n_train) * np.sum(residual * dp_dtheta)

        theta = theta - eta * grad

    queries = np.asarray(queries, dtype=float)
    m = queries.shape[0]
    return np.array([circuit_output(queries[k], theta, n, L) for k in range(m)])
