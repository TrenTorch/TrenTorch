import numpy as np


def mask_tokens(ids: np.ndarray, mask_id: int, vocab_size: int, special_ids: set, rng: np.random.RandomState, mask_prob: float = 0.15):
    """Returns (inputs, labels) with BERT-style 80/10/10 corruption; labels are -100 where not chosen."""
    # TODO
    pass
