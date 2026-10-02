"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

is_row_permutation_equivariant = load_solution(__file__).is_row_permutation_equivariant


def test_identity_permutation_is_trivially_equivariant():
    rng = np.random.default_rng(0)
    table = rng.normal(size=(4, 3, 5))
    row_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(5, 5)) for _ in range(3))
    identity = np.arange(4)
    assert is_row_permutation_equivariant(table, row_weights, col_weights, identity) is True


def test_a_genuine_shuffle_is_equivariant():
    rng = np.random.default_rng(1)
    table = rng.normal(size=(5, 3, 4))
    row_weights = tuple(rng.normal(size=(4, 4)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(4, 4)) for _ in range(3))
    permutation = rng.permutation(5)
    assert is_row_permutation_equivariant(table, row_weights, col_weights, permutation) is True


def test_holds_across_several_random_configurations():
    for seed in range(6):
        rng = np.random.default_rng(seed)
        n_rows = rng.integers(3, 8)
        table = rng.normal(size=(n_rows, rng.integers(2, 5), 4))
        row_weights = tuple(rng.normal(size=(4, 4)) for _ in range(3))
        col_weights = tuple(rng.normal(size=(4, 4)) for _ in range(3))
        permutation = rng.permutation(n_rows)
        assert is_row_permutation_equivariant(table, row_weights, col_weights, permutation) is True


def test_returns_a_plain_bool_not_a_numpy_bool_array():
    rng = np.random.default_rng(2)
    table = rng.normal(size=(3, 2, 3))
    row_weights = tuple(rng.normal(size=(3, 3)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(3, 3)) for _ in range(3))
    result = is_row_permutation_equivariant(table, row_weights, col_weights, np.array([2, 0, 1]))
    assert isinstance(result, bool)
