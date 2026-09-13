import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


def pooled_last_token_representation(hidden_states: np.ndarray, seq_len: int) -> np.ndarray:
    """
    A reward model scores a WHOLE response with a single number, so it
    needs one vector summarizing the entire sequence -- the standard
    choice is simply the LAST token's hidden state (by the final
    token, a causal transformer has already attended over everything
    before it).
    """
    # TODO: return hidden_states[seq_len - 1]
    pass


def reward_model_score(
    pooled_representation: np.ndarray, reward_head_weight: np.ndarray, reward_head_bias: np.ndarray
) -> float:
    """
    A reward model is a normal language model with one extra piece
    bolted on: a linear "reward head" mapping the pooled hidden state
    down to a single scalar score, instead of a vocab-sized
    next-token distribution.
    """
    # TODO: linear(pooled_representation, reward_head_weight,
    # reward_head_bias).item()
    pass


def reward_model_loss(chosen_reward: float, rejected_reward: float) -> float:
    """
    The Bradley-Terry pairwise preference loss used to train real
    reward models (InstructGPT/RLHF): -log(sigmoid(chosen_reward -
    rejected_reward)) -- low when the model correctly scores the
    chosen response higher, high when it gets the ranking backwards.
    """
    # TODO: sigmoid = 1 / (1 + exp(-(chosen_reward - rejected_reward))).
    # Return -log(sigmoid).
    pass
