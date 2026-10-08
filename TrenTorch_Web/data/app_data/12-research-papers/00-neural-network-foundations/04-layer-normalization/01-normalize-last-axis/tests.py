"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/04-layer-normalization/01-normalize-last-axis/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-layernorm-normalize")
normalize_last_axis = _module.normalize_last_axis


import numpy as np


def test_1_each_row_has_zero_mean():
    out = normalize_last_axis(np.array([[1.0, 2.0, 3.0], [10.0, 20.0, 30.0]]))
    np.testing.assert_allclose(out.mean(axis=-1), 0.0, atol=1e-9)


def test_2_each_row_has_unit_variance():
    out = normalize_last_axis(np.array([[1.0, 2.0, 3.0, 4.0]]))
    np.testing.assert_allclose(out.var(axis=-1), 1.0, atol=1e-4)


def test_3_single_example_is_normalized_on_its_own():
    out = normalize_last_axis(np.array([[5.0, 7.0]]), eps=0.0)
    np.testing.assert_allclose(out, [[-1.0, 1.0]])


def test_4_is_invariant_to_scaling_each_row():
    a = normalize_last_axis(np.array([[1.0, 2.0, 3.0]]))
    b = normalize_last_axis(np.array([[10.0, 20.0, 30.0]]))
    np.testing.assert_allclose(a, b, atol=1e-4)


def test_5_keeps_the_input_shape():
    assert normalize_last_axis(np.ones((2, 3, 4))).shape == (2, 3, 4)


def test_6_does_not_mutate_the_input():
    x = np.array([[1.0, 2.0]])
    normalize_last_axis(x)
    np.testing.assert_array_equal(x, [[1.0, 2.0]])

