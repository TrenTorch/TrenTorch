"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/11-llama/01-rmsnorm/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-llama-rmsnorm")
rmsnorm = _module.rmsnorm


import numpy as np


def test_1_unit_gain_gives_unit_root_mean_square():
    out = rmsnorm(np.array([[3.0, 4.0, 1.0, 2.0]]), np.ones(4), eps=0.0)
    np.testing.assert_allclose(np.sqrt(np.mean(out**2, axis=-1)), 1.0, atol=1e-9)


def test_2_gain_scales_each_feature():
    out = rmsnorm(np.array([[3.0, 4.0]]), np.array([2.0, 1.0]), eps=0.0)
    rms = np.sqrt((9 + 16) / 2)
    np.testing.assert_allclose(out, [[2 * 3 / rms, 4 / rms]])


def test_3_no_mean_subtraction():
    out = rmsnorm(np.array([[5.0, 5.0]]), np.ones(2), eps=0.0)
    np.testing.assert_allclose(out, [[1.0, 1.0]])


def test_4_zero_input_stays_zero():
    np.testing.assert_allclose(rmsnorm(np.zeros((1, 3)), np.ones(3)), 0.0)


def test_5_keeps_the_input_shape():
    assert rmsnorm(np.ones((2, 3, 4)), np.ones(4)).shape == (2, 3, 4)


def test_6_does_not_mutate_the_input():
    x = np.array([[1.0, 2.0]])
    rmsnorm(x, np.ones(2))
    np.testing.assert_array_equal(x, [[1.0, 2.0]])

