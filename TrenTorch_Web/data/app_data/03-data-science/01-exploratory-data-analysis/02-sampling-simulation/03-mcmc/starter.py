import numpy as np


def metropolis_hastings(log_target, x0: float, n_steps: int, step_size: float, rng: np.random.Generator) -> tuple:
    """
    log_target: function of a float returning the log density up to a
        constant (may return -inf outside the support)
    x0: starting point with log_target(x0) > -inf

    Each step draws step = rng.normal() and then u = rng.random(), in
    that order, proposes x_new = x + step_size * step and accepts when
    log(u) < log_target(x_new) - log_target(x). Records the state after
    each decision (a rejection repeats the previous value); x0 is not
    recorded.

    Returns:
        (samples, acceptance_rate): a float array of length n_steps and
        the fraction of accepted proposals as a float.
    """
    # TODO: Implement the random-walk Metropolis step from Theory.
    pass


def burn_in_and_thin(samples: np.ndarray, burn_in: int, thin: int) -> np.ndarray:
    """Returns samples[burn_in::thin] as a new array."""
    # TODO: Drop the early samples and keep every thin-th one.
    pass


def autocorrelation(samples: np.ndarray, lag: int) -> float:
    """
    Returns sum((x[t] - m) * (x[t + lag] - m)) / sum((x[t] - m) ** 2),
    with m the sample mean and t from 0 to n - lag - 1 in the numerator.
    1.0 at lag 0. Returns 0.0 if the sample has zero variance.
    """
    # TODO: Implement the formula from Theory.
    pass


def mcmc_effective_sample_size(samples: np.ndarray, max_lag: int) -> float:
    """
    Returns n / (1 + 2 * sum(rho_k)) with rho_k the autocorrelation at
    lag k, summing k = 1, 2, ... up to max_lag and stopping before the
    first negative autocorrelation. The result is clipped to [1, n].
    """
    # TODO: Discount the chain length by its autocorrelation.
    pass
