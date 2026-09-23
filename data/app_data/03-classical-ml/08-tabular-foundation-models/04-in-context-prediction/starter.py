import numpy as np


def build_incontext_table(
    train_features: np.ndarray, train_targets: np.ndarray, query_features: np.ndarray
) -> np.ndarray:
    """
    train_features: shape (n_train, n_features)
    train_targets:  shape (n_train,)
    query_features: shape (n_query, n_features)

    Returns:
        shape (n_train + n_query, n_features + 1, 1): one combined
        table. Training rows get a real target value in the last
        column. Query rows get 0 in that column, an explicit "unknown,
        to be predicted" marker, never a guess.
    """
    # TODO: n_rows = n_train + n_query. Build a zeros array of shape
    # (n_rows, n_features+1, 1). Fill the first n_train rows' first
    # n_features columns with train_features, and their LAST column
    # with train_targets. Fill the remaining n_query rows' first
    # n_features columns with query_features (their last column stays 0).
    pass


def in_context_predict(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    query_features: np.ndarray,
    row_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    col_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> np.ndarray:
    """
    Returns:
        shape (n_query,): a prediction for every query row, produced by
        ONE forward pass through 03's two_way_attention_block, no
        training loop, no gradient step, no per-dataset parameter
        update. The attention block's weights are fixed; only the
        table's CONTENT changes between different train/query sets.
    """
    # TODO: build_incontext_table(), run it through
    # two_way_attention_block(table, row_weights, col_weights), read
    # the query rows' target column (the last column, rows n_train
    # onward) off the output.
    pass
