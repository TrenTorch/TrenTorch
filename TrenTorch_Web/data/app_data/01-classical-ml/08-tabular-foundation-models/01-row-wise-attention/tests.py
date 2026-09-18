"""
pytest data/app_data/01-classical-ml/08-tabular-foundation-models/01-row-wise-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/08-tabular-foundation-models/{Path(__file__).resolve().parent.name}"
)
softmax = _module.softmax
scaled_dot_product_attention = _module.scaled_dot_product_attention
row_wise_attention = _module.row_wise_attention


def test_softmax_matches_hand_computation():
    x = np.array([1.0, 2.0, 3.0])
    result = softmax(x)
    exp_x = np.exp(x - x.max())
    expected = exp_x / exp_x.sum()
    assert np.allclose(result, expected)


def test_softmax_sums_to_one():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(4, 6))
    result = softmax(x, axis=-1)
    assert np.allclose(result.sum(axis=-1), 1.0)


def test_softmax_is_stable_for_large_values():
    x = np.array([1000.0, 1001.0, 1002.0])
    result = softmax(x)
    assert np.all(np.isfinite(result))
    assert np.isclose(result.sum(), 1.0)


def test_attention_output_is_a_convex_combination_of_value_rows():
    rng = np.random.default_rng(0)
    query = rng.normal(size=(2, 3))
    key = rng.normal(size=(4, 3))
    value = rng.normal(size=(4, 5))
    output = scaled_dot_product_attention(query, key, value)
    # every output row must be within value's own convex hull
    assert np.all(output.max(axis=0) <= value.max(axis=0) + 1e-8)
    assert np.all(output.min(axis=0) >= value.min(axis=0) - 1e-8)


def test_attention_matches_hand_computation():
    query = np.array([[1.0, 0.0]])
    key = np.array([[1.0, 0.0], [0.0, 1.0]])
    value = np.array([[10.0], [20.0]])
    result = scaled_dot_product_attention(query, key, value)
    scores = query @ key.T / np.sqrt(2)
    weights = np.exp(scores - scores.max()) / np.exp(scores - scores.max()).sum()
    expected = weights @ value
    assert np.allclose(result, expected)


def test_row_wise_attention_output_shape():
    rng = np.random.default_rng(0)
    table = rng.normal(size=(3, 4, 6))
    w_query, w_key, w_value = (rng.normal(size=(6, 6)) for _ in range(3))
    output = row_wise_attention(table, w_query, w_key, w_value)
    assert output.shape == (3, 4, 6)


def test_row_wise_attention_rows_are_independent():
    # Changing one row's cells must not affect any OTHER row's output --
    # attention here only ever mixes information within a single row.
    rng = np.random.default_rng(1)
    table = rng.normal(size=(3, 4, 5))
    w_query, w_key, w_value = (rng.normal(size=(5, 5)) for _ in range(3))
    output_before = row_wise_attention(table, w_query, w_key, w_value)

    table_changed = table.copy()
    table_changed[1] = rng.normal(size=(4, 5))
    output_after = row_wise_attention(table_changed, w_query, w_key, w_value)

    assert np.allclose(output_before[0], output_after[0])
    assert np.allclose(output_before[2], output_after[2])
    assert not np.allclose(output_before[1], output_after[1])


def test_scaling_by_sqrt_d_k_is_not_dropped():
    # Directly targets a mutant that forgets the /sqrt(d_k) scaling:
    # with high-dimensional queries/keys, unscaled dot products are
    # much larger in magnitude, pushing softmax toward a near-one-hot
    # distribution far more aggressively than the scaled version does.
    rng = np.random.default_rng(2)
    d_k = 64
    query = rng.normal(size=(1, d_k))
    key = rng.normal(size=(5, d_k))
    value = np.eye(5)  # identity value rows make the output literally BE the weights

    output = scaled_dot_product_attention(query, key, value)
    scores_scaled = query @ key.T / np.sqrt(d_k)
    weights_scaled = np.exp(scores_scaled - scores_scaled.max())
    weights_scaled /= weights_scaled.sum()

    assert np.allclose(output, weights_scaled)
    # a sanity check that scaling actually matters here: the unscaled
    # weights would be visibly more concentrated (higher max weight)
    scores_unscaled = query @ key.T
    weights_unscaled = np.exp(scores_unscaled - scores_unscaled.max())
    weights_unscaled /= weights_unscaled.sum()
    assert weights_unscaled.max() > weights_scaled.max()
