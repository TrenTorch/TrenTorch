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
    chosen_log_ratio = policy_chosen_logprob - ref_chosen_logprob
    rejected_log_ratio = policy_rejected_logprob - ref_rejected_logprob
    return beta * (chosen_log_ratio - rejected_log_ratio)


def dpo_loss(
    policy_chosen_logprob: np.ndarray,
    policy_rejected_logprob: np.ndarray,
    ref_chosen_logprob: np.ndarray,
    ref_rejected_logprob: np.ndarray,
    beta: float = 0.1,
) -> np.ndarray:
    margin = implicit_reward_margin(
        policy_chosen_logprob, policy_rejected_logprob, ref_chosen_logprob, ref_rejected_logprob, beta
    )
    return -np.log(_sigmoid(margin))
