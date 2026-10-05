import numpy as np


def _log_gaussian(X: np.ndarray, mean: np.ndarray, cov: np.ndarray) -> np.ndarray:
    d = X.shape[1]
    L = np.linalg.cholesky(cov)
    z = np.linalg.solve(L, (X - mean).T)
    maha = (z ** 2).sum(axis=0)
    log_det = 2.0 * np.log(np.diag(L)).sum()
    return -0.5 * (d * np.log(2 * np.pi) + log_det + maha)


def responsibilities(X: np.ndarray, means: np.ndarray, covs: np.ndarray, priors: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    means = np.asarray(means, dtype=float)
    covs = np.asarray(covs, dtype=float)
    priors = np.asarray(priors, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be 2-D")
    N, d = X.shape
    K = means.shape[0]
    if means.shape != (K, d) or covs.shape != (K, d, d) or priors.shape != (K,):
        raise ValueError("means, covs, and priors have inconsistent shapes")
    if np.any(priors <= 0) or not np.isclose(priors.sum(), 1.0):
        raise ValueError("priors must be strictly positive and sum to 1")
    try:
        log_joint = np.column_stack(
            [np.log(priors[k]) + _log_gaussian(X, means[k], covs[k]) for k in range(K)]
        )
    except np.linalg.LinAlgError as err:
        raise ValueError("each covariance must be positive definite") from err
    shifted = log_joint - log_joint.max(axis=1, keepdims=True)
    unnorm = np.exp(shifted)
    return unnorm / unnorm.sum(axis=1, keepdims=True)


def semi_supervised_e_step(
    X: np.ndarray,
    y: np.ndarray,
    means: np.ndarray,
    covs: np.ndarray,
    priors: np.ndarray,
) -> np.ndarray:
    R = responsibilities(X, means, covs, priors)
    y = np.asarray(y)
    K = R.shape[1]
    if y.shape != (R.shape[0],):
        raise ValueError("y must have one entry per row of X")
    if np.any((y < -1) | (y >= K)):
        raise ValueError("labels must be -1 or in 0..K-1")
    labeled = y >= 0
    R[labeled] = np.eye(K)[y[labeled]]
    return R
