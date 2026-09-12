import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

two_way_attention_block = load_solution(
    "01-classical-ml/08-tabular-foundation-models/03-two-way-attention-block"
).two_way_attention_block


def is_row_permutation_equivariant(
    table: np.ndarray,
    row_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    col_weights: tuple[np.ndarray, np.ndarray, np.ndarray],
    permutation: np.ndarray,
) -> bool:
    original_output = two_way_attention_block(table, row_weights, col_weights)

    permuted_table = table[permutation]
    permuted_output = two_way_attention_block(permuted_table, row_weights, col_weights)

    expected_output = original_output[permutation]
    return bool(np.allclose(permuted_output, expected_output, atol=1e-8))
