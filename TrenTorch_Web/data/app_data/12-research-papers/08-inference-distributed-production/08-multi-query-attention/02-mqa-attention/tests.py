"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/08-multi-query-attention/02-mqa-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mqa-attention")
multi_query_attention = _module.multi_query_attention


import numpy as np


def test_1_output_shape_matches_queries():
    out = multi_query_attention(np.ones((2, 3, 4)), np.ones((3, 4)), np.ones((3, 4)))
    assert out.shape == (2, 3, 4)


def test_2_identical_keys_average_the_values():
    V = np.array([[1.0], [3.0]])
    out = multi_query_attention(np.zeros((1, 1, 1)), np.zeros((2, 1)), V)
    np.testing.assert_allclose(out[0, 0], [2.0])


def test_3_each_head_uses_its_own_queries():
    rng = np.random.default_rng(0)
    q = rng.normal(size=(2, 3, 4))
    k = rng.normal(size=(3, 4))
    v = rng.normal(size=(3, 4))
    out = multi_query_attention(q, k, v)
    np.testing.assert_allclose(out[1], multi_query_attention(q[1:2], k, v)[0])


def test_4_output_rows_lie_in_value_hull():
    rng = np.random.default_rng(1)
    v = rng.normal(size=(4, 2))
    out = multi_query_attention(rng.normal(size=(1, 2, 3)), rng.normal(size=(4, 3)), v)
    assert np.all(out[0] >= v.min(axis=0) - 1e-9) and np.all(out[0] <= v.max(axis=0) + 1e-9)


def test_5_single_head_matches_standard_attention():
    rng = np.random.default_rng(2)
    q = rng.normal(size=(1, 2, 3))
    k = rng.normal(size=(2, 3))
    v = rng.normal(size=(2, 3))
    s = q[0] @ k.T / np.sqrt(3)
    w = np.exp(s - s.max(axis=-1, keepdims=True))
    w = w / w.sum(axis=-1, keepdims=True)
    np.testing.assert_allclose(multi_query_attention(q, k, v)[0], w @ v)


def test_6_does_not_mutate_inputs():
    q = np.ones((1, 1, 2))
    multi_query_attention(q, np.ones((1, 2)), np.ones((1, 2)))
    np.testing.assert_array_equal(q, np.ones((1, 1, 2)))

