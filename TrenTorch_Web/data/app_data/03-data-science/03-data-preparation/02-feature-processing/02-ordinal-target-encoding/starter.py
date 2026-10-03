import numpy as np


def ordinal_encode(values: np.ndarray, order: list) -> np.ndarray:
    """
    values: 1D array of labels
    order: list of labels from lowest to highest

    Returns:
        An int array: the position of each value in `order`, or -1 for a
        value that is not in `order`.
    """
    # TODO: Look each value up in a label-to-rank dict.
    pass


def target_encode(categories: np.ndarray, y: np.ndarray, smoothing: float = 0.0) -> dict:
    """
    categories: 1D array of labels
    y: 1D float array, same length

    Returns:
        A dict {category: (n * category_mean + smoothing * global_mean)
        / (n + smoothing)}, with n the number of rows of that category.
    """
    # TODO: Blend each category mean with the global mean, as in Theory.
    pass


def apply_target_encoding(categories: np.ndarray, mapping: dict, default: float) -> np.ndarray:
    """
    Returns:
        A float array with mapping[c] for each category c, or `default`
        for a category that is not in mapping.
    """
    # TODO: Look each category up, falling back to default.
    pass


def out_of_fold_target_encode(
    categories: np.ndarray, y: np.ndarray, n_folds: int, smoothing: float = 0.0
) -> np.ndarray:
    """
    Splits the indices into n_folds contiguous blocks with np.array_split
    (no shuffling). For each block, learns the mapping from all the other
    rows only and encodes the block with it, using the other rows' global
    mean as the default. Returns a float array of length len(y).
    """
    # TODO: Encode each block from the complement of that block.
    pass
