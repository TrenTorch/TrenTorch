"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/10-maxout-networks/02-maxout-argmax/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-maxout-argmax")
maxout_argmax = _module.maxout_argmax


import numpy as np


def test_1_output_shape_is_batch_by_out():
    idx = maxout_argmax(np.ones((5, 2)), np.ones((6, 2)), np.zeros(6), k=3)
    assert idx.shape == (5, 2)


def test_2_returns_the_index_of_the_largest_piece():
    x = np.array([[1.0]])
    W = np.array([[1.0], [5.0], [3.0]])
    np.testing.assert_array_equal(maxout_argmax(x, W, np.zeros(3), k=3), [[1]])


def test_3_indices_are_within_zero_to_k_minus_one():
    rng = np.random.default_rng(0)
    idx = maxout_argmax(rng.normal(size=(20, 3)), rng.normal(size=(12, 3)), np.zeros(12), k=4)
    assert idx.min() >= 0 and idx.max() <= 3


def test_4_bias_can_pick_a_different_piece():
    x = np.array([[0.0]])
    out = maxout_argmax(x, np.array([[1.0], [1.0]]), np.array([0.0, 2.0]), k=2)
    np.testing.assert_array_equal(out, [[1]])


def test_5_each_unit_picks_its_own_piece():
    x = np.array([[1.0]])
    W = np.array([[1.0], [0.0], [0.0], [1.0]])
    out = maxout_argmax(x, W, np.zeros(4), k=2)
    np.testing.assert_array_equal(out, [[0, 1]])


def test_6_argmax_matches_maxout_values():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(3, 2))
    W = rng.normal(size=(6, 2))
    b = rng.normal(size=6)
    idx = maxout_argmax(x, W, b, k=2)
    z = (x @ W.T + b).reshape(3, 3, 2)
    expected = np.take_along_axis(z, idx[..., None], axis=-1)[..., 0]
    np.testing.assert_allclose(expected, z.max(axis=-1))

