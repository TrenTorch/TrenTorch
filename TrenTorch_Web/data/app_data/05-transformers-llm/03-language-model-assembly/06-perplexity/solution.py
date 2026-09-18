import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

next_token_cross_entropy_loss = load_solution(
    "05-transformers-llm/03-language-model-assembly/03-next-token-cross-entropy"
).next_token_cross_entropy_loss


def perplexity(loss: float) -> float:
    return float(np.exp(loss))


def perplexity_from_logits(logits: np.ndarray, token_ids: np.ndarray) -> float:
    loss = next_token_cross_entropy_loss(logits, token_ids)
    return perplexity(loss)
