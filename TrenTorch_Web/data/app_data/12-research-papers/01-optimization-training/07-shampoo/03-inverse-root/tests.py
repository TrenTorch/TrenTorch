"""
pytest data/app_data/12-research-papers/01-optimization-and-training/07-shampoo/03-inverse-root/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-shampoo-inverse-root")
inverse_root = _module.inverse_root


import numpy as np


def test_1_fourth_root_of_sixteen_is_half():
    np.testing.assert_allclose(inverse_root(np.array([16.0]), 4), [0.5])


def test_2_fourth_root_of_eighty_one_is_one_third():
    np.testing.assert_allclose(inverse_root(np.array([81.0]), 4), [1.0 / 3.0])


def test_3_square_root_power_two():
    np.testing.assert_allclose(inverse_root(np.array([4.0]), 2), [0.5])


def test_4_keeps_the_shape():
    assert inverse_root(np.ones((2, 3)), 4).shape == (2, 3)


def test_5_larger_eigenvalue_gives_smaller_scale():
    out = inverse_root(np.array([2.0, 8.0]), 4)
    assert out[1] < out[0]


def test_6_returns_a_numpy_array():
    assert isinstance(inverse_root([16.0], 4), np.ndarray)

