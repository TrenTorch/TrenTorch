"""
pytest data/app_data/04-seq-modeling/02-embeddings/05-combine-token-positional-embeddings/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/02-embeddings/{Path(__file__).resolve().parent.name}")
combine_embeddings = _module.combine_embeddings


def test_output_shape_matches_token_embeddings_shape():
    token_embeddings = np.random.randn(4, 6, 8)
    positional_embeddings = np.random.randn(6, 8)
    result = combine_embeddings(token_embeddings, positional_embeddings)
    assert result.shape == (4, 6, 8)


def test_matches_hand_computation_for_a_single_sequence():
    token_embeddings = np.array([[[1.0, 2.0], [3.0, 4.0]]])  # (1, 2, 2)
    positional_embeddings = np.array([[10.0, 10.0], [20.0, 20.0]])  # (2, 2)
    result = combine_embeddings(token_embeddings, positional_embeddings)
    assert np.allclose(result, [[[11.0, 12.0], [23.0, 24.0]]])


def test_positional_embeddings_are_applied_identically_across_the_batch():
    token_embeddings = np.zeros((3, 2, 4))
    positional_embeddings = np.array([[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]])
    result = combine_embeddings(token_embeddings, positional_embeddings)
    for b in range(3):
        assert np.allclose(result[b], positional_embeddings)


def test_zero_positional_embeddings_leaves_token_embeddings_unchanged():
    token_embeddings = np.random.randn(2, 5, 3)
    positional_embeddings = np.zeros((5, 3))
    result = combine_embeddings(token_embeddings, positional_embeddings)
    assert np.allclose(result, token_embeddings)


def test_zero_token_embeddings_returns_just_the_positional_embeddings_broadcast():
    token_embeddings = np.zeros((2, 3, 4))
    positional_embeddings = np.random.randn(3, 4)
    result = combine_embeddings(token_embeddings, positional_embeddings)
    assert np.allclose(result[0], positional_embeddings)
    assert np.allclose(result[1], positional_embeddings)


def test_is_a_pure_addition_not_scaled_or_averaged():
    # Directly targets a mutant that averages the two inputs instead of
    # summing them ((a + b) / 2), which would halve the magnitude of the
    # combined result compared to a genuine sum.
    token_embeddings = np.ones((1, 1, 1)) * 3.0
    positional_embeddings = np.ones((1, 1)) * 4.0
    result = combine_embeddings(token_embeddings, positional_embeddings)
    assert np.isclose(result[0, 0, 0], 7.0)
