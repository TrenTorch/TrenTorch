import numpy as np


def metropolis_hastings(log_target, x0: float, n_steps: int, step_size: float, rng: np.random.Generator) -> tuple:
    x = float(x0)
    log_p = log_target(x)
    samples = np.empty(n_steps)
    accepted = 0
    for i in range(n_steps):
        step = rng.normal()
        u = rng.random()
        proposal = x + step_size * step
        log_p_proposal = log_target(proposal)
        if np.log(u) < log_p_proposal - log_p:
            x, log_p = proposal, log_p_proposal
            accepted += 1
        samples[i] = x
    return samples, float(accepted / n_steps)


def burn_in_and_thin(samples: np.ndarray, burn_in: int, thin: int) -> np.ndarray:
    return np.array(np.asarray(samples)[burn_in::thin])


def autocorrelation(samples: np.ndarray, lag: int) -> float:
    x = np.asarray(samples, dtype=float)
    centered = x - x.mean()
    denominator = float(np.sum(centered**2))
    if denominator == 0.0:
        return 0.0
    numerator = float(np.sum(centered[: len(x) - lag] * centered[lag:]))
    return numerator / denominator


def mcmc_effective_sample_size(samples: np.ndarray, max_lag: int) -> float:
    n = len(samples)
    total = 0.0
    for lag in range(1, max_lag + 1):
        rho = autocorrelation(samples, lag)
        if rho < 0:
            break
        total += rho
    return float(min(max(n / (1.0 + 2.0 * total), 1.0), n))
