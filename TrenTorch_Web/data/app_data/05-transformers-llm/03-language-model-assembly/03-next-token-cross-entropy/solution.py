import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

cross_entropy_forward = load_solution("02-deep-learning-core/03-losses/02-cross-entropy").cross_entropy_forward


def next_token_cross_entropy_loss(logits: np.ndarray, token_ids: np.ndarray) -> float:
    predicted_logits = logits[..., :-1, :]
    targets = token_ids[..., 1:]

    vocab_size = predicted_logits.shape[-1]
    flat_logits = predicted_logits.reshape(-1, vocab_size)
    flat_targets = targets.reshape(-1)

    return cross_entropy_forward(flat_logits, flat_targets)
