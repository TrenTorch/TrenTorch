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
    d_model = output_weight.shape[-1]
    predicted_hidden = hidden_states[..., :-1, :]
    targets = token_ids[..., 1:]

    flat_hidden = predicted_hidden.reshape(-1, d_model)
    flat_targets = targets.reshape(-1)

    logits = output_projection(flat_hidden, output_weight)
    loss = cross_entropy_forward(logits, flat_targets)
    grad_logits = cross_entropy_backward(logits, flat_targets)

    _, grad_output_weight, _ = linear_backward(grad_logits, flat_hidden, output_weight)
    return grad_output_weight, loss


def accumulate_gradients(gradients: list[np.ndarray]) -> np.ndarray:
    return np.mean(gradients, axis=0)


def train_with_gradient_accumulation(
    micro_batches: list[tuple[np.ndarray, np.ndarray]], output_weight: np.ndarray, lr: float
) -> tuple[np.ndarray, float]:
    gradients = []
    losses = []
    for hidden_states, token_ids in micro_batches:
        grad, loss = compute_output_head_gradient(hidden_states, token_ids, output_weight)
        gradients.append(grad)
        losses.append(loss)

    accumulated_grad = accumulate_gradients(gradients)
    updated_weight = output_weight - lr * accumulated_grad
    mean_loss = float(np.mean(losses))
    return updated_weight, mean_loss
