import numpy as np


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def implicit_reward_margin(
    policy_chosen_logprob: np.ndarray,
    policy_rejected_logprob: np.ndarray,
    ref_chosen_logprob: np.ndarray,
    ref_rejected_logprob: np.ndarray,
    beta: float,
) -> np.ndarray:
    """
    DPO's key trick: instead of training a separate reward model, it
    treats "how much MORE likely the policy makes a response relative
    to the frozen reference model" as an IMPLICIT reward. This margin
    is beta * [(log pi(chosen) - log ref(chosen)) - (log pi(rejected) -
    log ref(rejected))] -- how much more the policy has increased the
    chosen response's likelihood (relative to the reference) compared
    to the rejected one.
    """
    # TODO: chosen_log_ratio = policy_chosen_logprob - ref_chosen_logprob.
    # rejected_log_ratio = policy_rejected_logprob - ref_rejected_logprob.
    # Return beta * (chosen_log_ratio - rejected_log_ratio).
    pass


def dpo_loss(
    policy_chosen_logprob: np.ndarray,
    policy_rejected_logprob: np.ndarray,
    ref_chosen_logprob: np.ndarray,
    ref_rejected_logprob: np.ndarray,
    beta: float = 0.1,
) -> np.ndarray:
    """
    The DPO loss (Rafailov et al., 2023): -log(sigmoid(margin)), the
    SAME Bradley-Terry-shaped loss 04-reward-modeling-bradley-terry
    uses -- except here the "reward difference" being optimized is the
    implicit_reward_margin computed directly from log-probabilities,
    with NO separate reward model and NO RL rollout loop at all.
    """
    # TODO: margin = implicit_reward_margin(...). Return
    # -log(sigmoid(margin)).
    pass
