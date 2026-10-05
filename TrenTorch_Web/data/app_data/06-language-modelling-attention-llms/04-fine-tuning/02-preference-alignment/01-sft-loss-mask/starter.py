import numpy as np


def response_mask(prompt_lens: np.ndarray, seq_lens: np.ndarray, T: int) -> np.ndarray:
    """(B, T) boolean mask, True where prompt_lens[b] <= t < seq_lens[b]."""
    # TODO: Compare np.arange(T) against both boundaries with broadcasting.
    pass


def sft_loss(logits: np.ndarray, token_ids: np.ndarray, prompt_lens: np.ndarray, seq_lens: np.ndarray) -> float:
    """
    Mean next-token NLL over response tokens only. logits[b, t] predicts
    token_ids[b, t + 1].
    """
    # TODO: Shift logits and targets, log-softmax, gather, mask, average.
    pass
