import numpy as np


def kl_penalized_rewards(logp_policy, logp_ref, final_reward, lengths, beta: float) -> np.ndarray:
    """(B, T) per-token rewards: KL penalty everywhere valid, plus the final reward on the last valid token."""
    # TODO
    pass


def mean_kl(logp_policy, logp_ref, lengths) -> float:
    """Mean of (logp_policy - logp_ref) over valid tokens."""
    # TODO
    pass
