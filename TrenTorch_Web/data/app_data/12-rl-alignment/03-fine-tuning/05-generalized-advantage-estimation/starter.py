import numpy as np


def td_residuals(rewards: np.ndarray, values: np.ndarray, next_values: np.ndarray, dones: np.ndarray, gamma: float) -> np.ndarray:
    """
    The one-step TD (temporal-difference) residual at each timestep:
    delta[t] = reward[t] + gamma * next_value[t] * (1 - done[t]) -
    value[t]. Positive when the outcome was better than the value
    function predicted; negative when worse. `(1 - done[t])` zeroes
    out the bootstrap term at an episode's final step, since there's
    no valid "next state" to bootstrap from there.
    """
    # TODO: implement the formula above, elementwise across the arrays.
    pass


def generalized_advantage_estimation(
    rewards: np.ndarray, values: np.ndarray, next_values: np.ndarray, dones: np.ndarray, gamma: float, lam: float
) -> np.ndarray:
    """
    GAE (Schulman et al., 2016): an exponentially-weighted average of
    TD residuals looking further and further into the future,
    computed efficiently via ONE backward recursive pass:
    advantage[t] = delta[t] + gamma * lam * (1 - done[t]) *
    advantage[t+1] (with advantage past the end treated as 0).
    `lam=0` reduces to the plain one-step TD residual; `lam=1` reduces
    to the full Monte-Carlo advantage (discounted return minus value).
    """
    # TODO: compute deltas via td_residuals. Loop t from the LAST
    # index down to 0, maintaining running = deltas[t] + gamma * lam *
    # (1 - dones[t]) * running (running starts at 0.0), storing
    # running into advantages[t] each step.
    pass
