
import numpy as np

from _load import load_solution

next_token_cross_entropy_loss = load_solution("txf-lm-next-token-cross-entropy").next_token_cross_entropy_loss


def perplexity(loss: float) -> float:
    """
    Perplexity: `exp(loss)`, where `loss` is the average (mean-reduced)
    next-token Cross-Entropy loss, `[03-next-token-cross-entropy]`'s
    `next_token_cross_entropy_loss`.
    """
    pass


def perplexity_from_logits(logits: np.ndarray, token_ids: np.ndarray) -> float:
    """
    Computes `[03-next-token-cross-entropy]`'s loss directly from logits
    and token ids, then converts it to perplexity.
    """
    pass
