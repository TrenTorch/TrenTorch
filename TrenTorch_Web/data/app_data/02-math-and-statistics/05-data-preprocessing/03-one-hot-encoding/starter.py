import numpy as np


def get_unique_categories(column: np.ndarray) -> np.ndarray:
    """
    Returns every distinct value appearing in `column`, in a fixed,
    reproducible order (np.unique sorts its output, which is what
    makes one_hot_encode's column ordering deterministic run to run).
    """
    pass


def one_hot_encode(column: np.ndarray, categories: np.ndarray | None = None) -> np.ndarray:
    """
    Converts a length-n categorical column into an (n, k) binary
    matrix, where k is the number of distinct categories: row i has a
    single 1 in the column matching column[i]'s category, and 0s
    everywhere else.

    `categories` (a fixed, ordered list of category values) can be
    supplied explicitly, use get_unique_categories(column) if it's
    None. See Theory for why supplying it explicitly, rather than
    always deriving it fresh, matters for real train/test pipelines.
    """
    pass
