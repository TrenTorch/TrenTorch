import numpy as np


def gaussian_pdf(x, mu, sigma):
    x = np.array(x, dtype=float)
    coeff = 1.0 / (sigma * np.sqrt(2 * np.pi))
    exponent = -((x - mu) ** 2) / (2 * sigma**2)
    return coeff * np.exp(exponent)


def sample_gaussian(mu, sigma, n, uniform_draws):
    u = np.array(uniform_draws, dtype=float)
    u1, u2 = u[0::2], u[1::2]
    u1 = np.clip(u1, 1e-12, None)

    r = np.sqrt(-2.0 * np.log(u1))
    theta = 2.0 * np.pi * u2
    z0 = r * np.cos(theta)
    z1 = r * np.sin(theta)

    z = np.empty(2 * len(u1))
    z[0::2], z[1::2] = z0, z1

    return mu + sigma * z[:n]
