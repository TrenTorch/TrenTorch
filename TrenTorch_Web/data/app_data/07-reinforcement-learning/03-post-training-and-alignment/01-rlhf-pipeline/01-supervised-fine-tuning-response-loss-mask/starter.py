
import numpy as np

from _load import load_solution

cross_entropy_forward = load_solution("dl-core-cross-entropy-loss").cross_entropy_forward


def make_response_mask(prompt_len: int, total_len: int) -> np.ndarray:
    """
    A boolean mask of length total_len, True for every position at or
    after prompt_len (the response tokens) and False before it (the
    prompt tokens).
    """
    # TODO: build a length-total_len boolean array, all False, then set
    # positions [prompt_len:] to True.
    pass


def sft_loss(logits: np.ndarray, targets: np.ndarray, prompt_len: int) -> float:
    """
    Ordinary next-token cross-entropy loss (dl-core-cross-entropy-loss's
    formula), but averaged ONLY over the response positions -- the
    prompt tokens contribute zero to the loss, since the model isn't
    being trained to "predict" the prompt it was given.
    """
    # TODO: compute per-token loss with cross_entropy_forward(...,
    # reduction="none"), build the response mask, and average only the
    # masked (response) entries.
    pass


def raw_pretraining_loss(logits: np.ndarray, targets: np.ndarray) -> float:
    """
    Plain next-token loss averaged over EVERY position -- what raw
    (unsupervised) pretraining optimizes, with no notion of "prompt"
    vs "response" at all.
    """
    # TODO: cross_entropy_forward(logits, targets, reduction="mean")
    pass
