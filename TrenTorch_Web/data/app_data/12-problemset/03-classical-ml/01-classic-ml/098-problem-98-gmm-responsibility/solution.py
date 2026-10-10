import numpy as np

def gaussian_logpdf(x, mean, cov):
    x = np.atleast_1d(np.asarray(x, dtype=float))
    mean = np.atleast_1d(np.asarray(mean, dtype=float))
    cov = np.atleast_2d(np.asarray(cov, dtype=float))
    diff = x - mean
    _, logdet = np.linalg.slogdet(cov)
    maha = diff @ np.linalg.solve(cov, diff)
    return -0.5 * (x.shape[0] * np.log(2 * np.pi) + logdet + maha)

def solve(x, weights, means, covs):
    logs = np.array([np.log(w) + gaussian_logpdf(x, m, c) for w, m, c in zip(weights, means, covs)])
    z = np.max(logs)
    q = np.exp(logs - z)
    return q / q.sum()
