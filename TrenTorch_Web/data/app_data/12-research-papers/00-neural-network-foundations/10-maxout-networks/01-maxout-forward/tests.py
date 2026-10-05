"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/10-maxout-networks/01-maxout-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-maxout-forward")
maxout_forward = _module.maxout_forward


import numpy as np


def test_1_output_shape_is_batch_by_out():
    out = maxout_forward(np.ones((4, 3)), np.ones((6, 3)), np.zeros(6), k=2)
    assert out.shape == (4, 3)


def test_2_takes_the_max_over_the_pieces():
    x = np.array([[2.0]])
    W = np.array([[1.0], [3.0]])
    out = maxout_forward(x, W, np.zeros(2), k=2)
    np.testing.assert_allclose(out, [[6.0]])


def test_3_single_piece_is_a_plain_linear_unit():
    x = np.array([[2.0]])
    out = maxout_forward(x, np.array([[4.0]]), np.array([1.0]), k=1)
    np.testing.assert_allclose(out, [[9.0]])


def test_4_bias_can_change_the_winning_piece():
    x = np.array([[1.0]])
    out = maxout_forward(x, np.array([[1.0], [1.0]]), np.array([0.0, 5.0]), k=2)
    np.testing.assert_allclose(out, [[6.0]])


def test_5_pieces_are_grouped_per_unit():
    x = np.array([[1.0]])
    W = np.array([[1.0], [2.0], [3.0], [4.0]])
    out = maxout_forward(x, W, np.zeros(4), k=2)
    np.testing.assert_allclose(out, [[2.0, 4.0]])


def test_6_does_not_mutate_inputs():
    x = np.ones((1, 2))
    maxout_forward(x, np.eye(2), np.zeros(2), k=1)
    np.testing.assert_array_equal(x, np.ones((1, 2)))

