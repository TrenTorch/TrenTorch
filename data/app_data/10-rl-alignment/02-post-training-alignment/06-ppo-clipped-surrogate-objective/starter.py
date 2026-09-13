import numpy as np


def probability_ratio(new_log_prob: np.ndarray, old_log_prob: np.ndarray) -> np.ndarray:
    """
    How much more (or less) likely the CURRENT policy is to produce a
    given action than the policy that actually collected the data:
    exp(new_log_prob - old_log_prob). Equal to 1.0 when the policy
    hasn't changed at all since the data was collected.
    """
    # TODO: np.exp(new_log_prob - old_log_prob)
    pass


def ppo_clipped_surrogate_loss(ratio: np.ndarray, advantage: np.ndarray, epsilon: float = 0.2) -> np.ndarray:
    """
    PPO's clipped surrogate objective (Schulman et al., 2017): takes
    the MORE PESSIMISTIC of an unclipped and a clipped estimate, so a
    single update step can't move the policy arbitrarily far from
    where the data was actually collected -- returns the LOSS (i.e.
    the negative of the objective, since it's meant to be minimized).
    """
    # TODO: unclipped = ratio * advantage. clipped = np.clip(ratio, 1 -
    # epsilon, 1 + epsilon) * advantage. Return
    # -np.minimum(unclipped, clipped).
    pass


def fraction_of_ratios_clipped(ratio: np.ndarray, epsilon: float = 0.2) -> float:
    """
    What fraction of a batch's probability ratios actually got clipped
    (fell outside [1 - epsilon, 1 + epsilon]) -- a real, commonly
    logged PPO training diagnostic for how aggressively the policy is
    trying to change.
    """
    # TODO: mean of (ratio < 1 - epsilon) | (ratio > 1 + epsilon)
    pass
