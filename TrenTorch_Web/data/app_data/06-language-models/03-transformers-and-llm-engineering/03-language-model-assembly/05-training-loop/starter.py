
import numpy as np

from _load import load_solution

output_projection = load_solution("txf-lm-output-projection").output_projection
linear_backward = load_solution("dl-training-linear-backward").linear_backward
_losses = load_solution("dl-core-cross-entropy-loss")
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
    (mirroring `[05-deep-learning/02-training-and-sequence-models/03-training-loop/02-assemble-training-loop]`'s
    own single-linear-layer scope): treats `hidden_states` (the rest of
    the model's output) as FIXED input features, computes next-token
    Cross-Entropy loss and its gradient, backpropagates through
    `[01-output-projection]`'s linear projection only (via
    `[05-deep-learning/02-training-and-sequence-models/02-layers/02-linear-backward]`'s `linear_backward`),
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
