import numpy as np

def solve(x, mu, sigma, pi):
    x = float(x)
    mu = np.asarray(mu, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    pi = np.asarray(pi, dtype=float)
    with np.errstate(divide="ignore"):
        log_q = np.log(pi) - np.log(sigma) - 0.5 * ((x - mu) / sigma) ** 2
    q = np.exp(log_q - log_q.max())
    return q / q.sum()
