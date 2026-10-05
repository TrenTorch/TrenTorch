
import numpy as np

from _load import load_solution

cross_entropy_forward = load_solution("dl-core-cross-entropy-loss").cross_entropy_forward


def next_token_cross_entropy_loss(logits: np.ndarray, token_ids: np.ndarray) -> float:
    """
    Next-token prediction loss: position `t`'s logits should predict the
    token that actually occurs at position `t + 1`, so this SHIFTS the
    logits and targets by one position relative to each other before
    calling `[05-deep-learning/01-core-mechanics/03-losses/02-cross-entropy]`'s
    `cross_entropy_forward`.

    `logits`: `(..., seq_len, vocab_size)`. `token_ids`: `(..., seq_len)`,
    integer token ids.
    """
    pass
