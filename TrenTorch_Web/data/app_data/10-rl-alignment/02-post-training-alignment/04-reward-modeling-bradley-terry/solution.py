import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


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
