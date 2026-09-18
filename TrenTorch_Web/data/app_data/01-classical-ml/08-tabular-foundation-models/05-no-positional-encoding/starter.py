import numpy as np


def is_row_permutation_equivariant(
    table: np.ndarray,
    row_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    col_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    permutation: np.ndarray,
) -> bool:
    """
    permutation: shape (n_rows,), a permutation of 0..n_rows-1.

    Checks that running two_way_attention_block on a row-shuffled
    table gives exactly the same output as running it on the original
    table and THEN applying that same row shuffle: shuffling the input
    rows and shuffling the output rows are interchangeable.

    Returns:
        True if that property holds (within floating-point tolerance).
    """
    # TODO: Run two_way_attention_block on `table` to get the original
    # output. Run it again on `table[permutation]` (the row-shuffled
    # table) to get the permuted output. Compare the permuted output
    # against original_output[permutation] -- they should match.
    pass
