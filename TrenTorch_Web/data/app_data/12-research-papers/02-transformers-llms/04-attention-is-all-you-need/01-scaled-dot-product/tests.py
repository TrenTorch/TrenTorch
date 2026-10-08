"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/04-attention-is-all-you-need/01-scaled-dot-product/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-scaled-dot-attention")
scaled_dot_product_attention = _module.scaled_dot_product_attention


import numpy as np


def test_1_output_shape_is_queries_by_value_dim():
    out = scaled_dot_product_attention(np.ones((2, 4)), np.ones((5, 4)), np.ones((5, 3)))
    assert out.shape == (2, 3)


def test_2_identical_keys_average_the_values():
    V = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 2.0]])
    out = scaled_dot_product_attention(np.ones((1, 2)), np.zeros((3, 2)), V)
    np.testing.assert_allclose(out, [V.mean(axis=0)])


def test_3_matches_a_hand_computed_case():
    Q = np.array([[1.0, 0.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0]])
    V = np.array([[1.0, 0.0], [0.0, 1.0]])
    a = np.exp(1 / np.sqrt(2))
    np.testing.assert_allclose(scaled_dot_product_attention(Q, K, V), [[a / (a + 1), 1 / (a + 1)]], atol=1e-12)


def test_4_each_output_row_is_inside_the_value_hull():
    rng = np.random.default_rng(0)
    V = rng.normal(size=(6, 2))
    out = scaled_dot_product_attention(rng.normal(size=(3, 4)), rng.normal(size=(6, 4)), V)
    assert np.all(out.min(axis=0) >= V.min(axis=0) - 1e-9)
    assert np.all(out.max(axis=0) <= V.max(axis=0) + 1e-9)


def test_5_scaling_by_sqrt_d_keeps_scores_moderate():
    d = 256
    rng = np.random.default_rng(1)
    Q = rng.normal(size=(1, d))
    K = rng.normal(size=(8, d))
    raw = Q @ K.T
    scaled = raw / np.sqrt(d)
    assert scaled.std() < raw.std()


def test_6_does_not_mutate_inputs():
    Q = np.ones((1, 2))
    scaled_dot_product_attention(Q, np.ones((2, 2)), np.ones((2, 2)))
    np.testing.assert_array_equal(Q, np.ones((1, 2)))

