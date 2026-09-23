import numpy as np

R_H = 1.097373e7  # m^-1, fixed by the problem -- do not substitute a different value


def rydberg_wavelength_nm(n1: int, n2: int) -> float:
    inv_lambda_m = R_H * (1.0 / n1**2 - 1.0 / n2**2)
    return (1.0 / inv_lambda_m) * 1e9


def _forward_substitution(L: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = L.shape[0]
    z = np.zeros(n)
    for i in range(n):
        z[i] = (b[i] - L[i, :i] @ z[:i]) / L[i, i]
    return z


def _back_substitution(U: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = U.shape[0]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - U[i, i + 1 :] @ x[i + 1 :]) / U[i, i]
    return x


def gp_calibrate(
    training: list[tuple[int, int, float]],
    sigma_f: float,
    l: float,
    sigma_n: float,
    queries: list[tuple[int, int]],
) -> np.ndarray:
    n = len(training)
    x = np.array([rydberg_wavelength_nm(n1, n2) for n1, n2, _ in training])
    y = np.array([measured - xi for (n1, n2, measured), xi in zip(training, x)])

    K = sigma_f**2 * np.exp(-((x[:, None] - x[None, :]) ** 2) / (2 * l**2))
    L = np.linalg.cholesky(K + sigma_n**2 * np.eye(n))
    alpha = _back_substitution(L.T, _forward_substitution(L, y))

    results = []
    for q_n1, q_n2 in queries:
        x_star = rydberg_wavelength_nm(q_n1, q_n2)
        k_star = sigma_f**2 * np.exp(-((x - x_star) ** 2) / (2 * l**2))

        mu = float(k_star @ alpha)
        v = _forward_substitution(L, k_star)
        var = max(sigma_f**2 - float(v @ v), 0.0)  # guard against a tiny negative from floating point

        results.append((x_star + mu, np.sqrt(var)))

    return np.array(results)
