import numpy as np


def advance(transitions: dict, state, token: str):
    """Feed token's characters through the machine; return the final state or None if invalid."""
    # TODO
    pass


def allowed_token_ids(transitions: dict, state, vocab: list[str]) -> list[int]:
    """Sorted ids of non-empty tokens that keep the machine valid."""
    # TODO
    pass


def mask_logits(logits: np.ndarray, allowed: list[int]) -> np.ndarray:
    """Copy of logits with -inf everywhere except at the allowed ids."""
    # TODO
    pass
