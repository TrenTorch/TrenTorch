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
    d_model = output_weight.shape[-1]

    predicted_hidden = hidden_states[..., :-1, :]
    targets = token_ids[..., 1:]

    flat_hidden = predicted_hidden.reshape(-1, d_model)
    flat_targets = targets.reshape(-1)

    logits = output_projection(flat_hidden, output_weight)
    loss = cross_entropy_forward(logits, flat_targets)
    grad_logits = cross_entropy_backward(logits, flat_targets)

    _, grad_output_weight, _ = linear_backward(grad_logits, flat_hidden, output_weight)

    updated_output_weight = output_weight - lr * grad_output_weight
    return updated_output_weight, loss


def train_output_head(
    hidden_states: np.ndarray,
    token_ids: np.ndarray,
    output_weight: np.ndarray,
    lr: float,
    num_steps: int,
) -> tuple[np.ndarray, list[float]]:
    loss_history = []
    for _ in range(num_steps):
        output_weight, loss = train_output_head_one_step(hidden_states, token_ids, output_weight, lr)
        loss_history.append(loss)
    return output_weight, loss_history
