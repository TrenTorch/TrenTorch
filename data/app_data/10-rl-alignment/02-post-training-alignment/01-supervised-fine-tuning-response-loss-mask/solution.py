import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

cross_entropy_forward = load_solution("02-deep-learning-core/03-losses/02-cross-entropy").cross_entropy_forward


def make_response_mask(prompt_len: int, total_len: int) -> np.ndarray:
    mask = np.zeros(total_len, dtype=bool)
    mask[prompt_len:] = True
    return mask


def sft_loss(logits: np.ndarray, targets: np.ndarray, prompt_len: int) -> float:
    total_len = logits.shape[0]
    mask = make_response_mask(prompt_len, total_len)
    per_token_loss = cross_entropy_forward(logits, targets, reduction="none")
    return float(per_token_loss[mask].mean())


def raw_pretraining_loss(logits: np.ndarray, targets: np.ndarray) -> float:
    return float(cross_entropy_forward(logits, targets, reduction="mean"))
