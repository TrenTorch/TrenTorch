import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

output_projection = load_solution("05-transformers-llm/03-language-model-assembly/01-output-projection").output_projection
linear_backward = load_solution("03-dl-training/02-layers/02-linear-backward").linear_backward
_losses = load_solution("02-deep-learning-core/03-losses/02-cross-entropy")
cross_entropy_forward = _losses.cross_entropy_forward
cross_entropy_backward = _losses.cross_entropy_backward


def train_output_head_one_step(
    hidden_states: np.ndarray,
    token_ids: np.ndarray,
    output_weight: np.ndarray,
    lr: float,
) -> tuple[np.ndarray, float]:
    """
    One SGD step of REAL backpropagation, scoped to the output head
    (mirroring `[03-dl-training/03-training-loop/02-assemble-training-loop]`'s
    own single-linear-layer scope): treats `hidden_states` (the rest of
    the model's output) as FIXED input features, computes next-token
    Cross-Entropy loss and its gradient, backpropagates through
    `[01-output-projection]`'s linear projection only (via
    `[03-dl-training/02-layers/02-linear-backward]`'s `linear_backward`),
    and returns the updated `output_weight` and the loss BEFORE the update.
    """
    pass


def train_output_head(
    hidden_states: np.ndarray,
    token_ids: np.ndarray,
    output_weight: np.ndarray,
    lr: float,
    num_steps: int,
) -> tuple[np.ndarray, list[float]]:
    """
    Runs `train_output_head_one_step` repeatedly, returning the final
    `output_weight` and the full per-step loss history (expected to
    generally DECREASE across steps, since each step is a genuine
    gradient-descent update).
    """
    pass
