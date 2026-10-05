
import numpy as np

from _load import load_solution

next_token_cross_entropy_loss = load_solution("txf-lm-next-token-cross-entropy").next_token_cross_entropy_loss


def perplexity(loss: float) -> float:
    return float(np.exp(loss))


def perplexity_from_logits(logits: np.ndarray, token_ids: np.ndarray) -> float:
    loss = next_token_cross_entropy_loss(logits, token_ids)
    return perplexity(loss)
