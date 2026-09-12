import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

cross_entropy_forward = load_solution("02-deep-learning-core/03-losses/02-cross-entropy").cross_entropy_forward


def next_token_cross_entropy_loss(logits: np.ndarray, token_ids: np.ndarray) -> float:
    """
    Next-token prediction loss: position `t`'s logits should predict the
    token that actually occurs at position `t + 1`, so this SHIFTS the
    logits and targets by one position relative to each other before
    calling `[02-deep-learning-core/03-losses/02-cross-entropy]`'s
    `cross_entropy_forward`.

    `logits`: `(..., seq_len, vocab_size)`. `token_ids`: `(..., seq_len)`,
    integer token ids.
    """
    pass
