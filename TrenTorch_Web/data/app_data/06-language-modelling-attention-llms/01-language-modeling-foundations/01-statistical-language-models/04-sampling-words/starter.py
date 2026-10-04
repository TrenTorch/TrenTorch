import numpy as np


def sample_word(probs: np.ndarray, itos: list[str], rng: np.random.RandomState, max_len: int = 50) -> str:
    """
    Generates one word by walking the bigram table from the boundary
    symbol, one `rng.random_sample()` per step, until the boundary is
    drawn or `max_len` characters exist.
    """
    # TODO: Draw by inverse-transform sampling from the current row.
    pass
