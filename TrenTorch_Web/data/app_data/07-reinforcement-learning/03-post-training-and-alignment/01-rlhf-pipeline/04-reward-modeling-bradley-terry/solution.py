
import numpy as np

from _load import load_solution

linear = load_solution("linear-regression-hypothesis-function").linear


def pooled_last_token_representation(hidden_states: np.ndarray, seq_len: int) -> np.ndarray:
    return hidden_states[seq_len - 1]


def reward_model_score(
    pooled_representation: np.ndarray, reward_head_weight: np.ndarray, reward_head_bias: np.ndarray
) -> float:
    return linear(pooled_representation, reward_head_weight, reward_head_bias).item()


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def reward_model_loss(chosen_reward: float, rejected_reward: float) -> float:
    return float(-np.log(_sigmoid(chosen_reward - rejected_reward)))
