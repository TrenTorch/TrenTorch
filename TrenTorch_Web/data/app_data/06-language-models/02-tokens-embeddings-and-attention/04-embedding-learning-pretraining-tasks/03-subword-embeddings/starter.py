import numpy as np


def char_ngrams(word: str, n_min: int, n_max: int) -> list[str]:
    """Character n-grams of '<word>' for n in [n_min, n_max], then the wrapped word itself."""
    # TODO
    pass


def subword_embedding(word: str, table: dict, n_min: int, n_max: int, dim: int) -> np.ndarray:
    """Mean of the table vectors for the word's known n-grams (zeros if none)."""
    # TODO
    pass
