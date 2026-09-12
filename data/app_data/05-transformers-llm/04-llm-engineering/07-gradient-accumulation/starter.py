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


def compute_output_head_gradient(
    hidden_states: np.ndarray, token_ids: np.ndarray, output_weight: np.ndarray
) -> tuple[np.ndarray, float]:
    """
    `[03-language-model-assembly/05-training-loop]`'s
    `train_output_head_one_step`, minus the weight UPDATE: computes and
    returns just the gradient and the loss, for ONE micro-batch.
    """
    pass


def accumulate_gradients(gradients: list[np.ndarray]) -> np.ndarray:
    """
    Combines several micro-batches' gradients into ONE gradient, as if
    they'd all been computed on a single larger batch: the elementwise
    MEAN (not sum) across all the micro-batch gradients, matching a
    mean-reduced loss's own averaging convention.
    """
    pass


def train_with_gradient_accumulation(
    micro_batches: list[tuple[np.ndarray, np.ndarray]], output_weight: np.ndarray, lr: float
) -> tuple[np.ndarray, float]:
    """
    Computes each micro-batch's OWN gradient (without updating the
    weights in between), accumulates them via `accumulate_gradients`,
    and applies exactly ONE weight update using the combined gradient,
    simulating a large batch that wouldn't otherwise fit in memory all
    at once.
    """
    pass
