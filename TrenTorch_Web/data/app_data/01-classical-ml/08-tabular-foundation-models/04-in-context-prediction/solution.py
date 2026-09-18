import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

two_way_attention_block = load_solution(
    "01-classical-ml/08-tabular-foundation-models/03-two-way-attention-block"
).two_way_attention_block


def build_incontext_table(
    train_features: np.ndarray, train_targets: np.ndarray, query_features: np.ndarray
) -> np.ndarray:
    n_train, n_features = train_features.shape
    n_query = query_features.shape[0]
    n_rows = n_train + n_query

    table = np.zeros((n_rows, n_features + 1, 1))
    table[:n_train, :n_features, 0] = train_features
    table[:n_train, n_features, 0] = train_targets
    table[n_train:, :n_features, 0] = query_features
    # target column for query rows stays 0: unknown, masked, not "predicted as 0"

    return table


def in_context_predict(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    query_features: np.ndarray,
    row_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    col_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> np.ndarray:
    table = build_incontext_table(train_features, train_targets, query_features)
    output = two_way_attention_block(table, row_weights, col_weights)

    n_train = train_features.shape[0]
    return output[n_train:, -1, 0]
