import numpy as np

def gaussian_logpdf(x, mu, cov):
    x, mu, S = (np.asarray(x, float), np.asarray(mu, float), np.asarray(cov, float))
    d = len(x)
    sign, ld = np.linalg.slogdet(S)
    if sign <= 0:
        raise ValueError('covariance must be positive definite')
    delta = x - mu
    return float(-0.5 * (d * np.log(2 * np.pi) + ld + delta @ np.linalg.solve(S, delta)))

def solve(x, weights, means, covs):
    """Implement gmm responsibility according to the contract."""
    logs = np.array([np.log(w) + gaussian_logpdf(x, m, c) for w, m, c in zip(weights, means, covs)])
    q = np.exp(logs - np.max(logs))
    return q / q.sum()
