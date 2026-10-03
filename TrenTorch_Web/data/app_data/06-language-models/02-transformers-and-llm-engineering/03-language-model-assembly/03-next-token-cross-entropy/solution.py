
import numpy as np

from _load import load_solution

cross_entropy_forward = load_solution("dl-core-cross-entropy-loss").cross_entropy_forward


def next_token_cross_entropy_loss(logits: np.ndarray, token_ids: np.ndarray) -> float:
    predicted_logits = logits[..., :-1, :]
    targets = token_ids[..., 1:]

    vocab_size = predicted_logits.shape[-1]
    flat_logits = predicted_logits.reshape(-1, vocab_size)
    flat_targets = targets.reshape(-1)

    return cross_entropy_forward(flat_logits, flat_targets)
