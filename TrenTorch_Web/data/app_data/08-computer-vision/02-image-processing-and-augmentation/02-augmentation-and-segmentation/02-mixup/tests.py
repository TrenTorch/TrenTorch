"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
sample_lambda = _module.sample_lambda
mixup = _module.mixup


def test_1_hand_computed_mix():
    x, y = mixup(np.array([1.0, 3.0]), np.array([1.0, 0.0]), np.array([5.0, 7.0]), np.array([0.0, 1.0]), 0.25)
    assert np.allclose(x, [4.0, 6.0]) and np.allclose(y, [0.25, 0.75])


def test_2_endpoints_return_the_parents():
    a, b = np.random.RandomState(0).rand(3, 3), np.random.RandomState(1).rand(3, 3)
    ya, yb = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    x, y = mixup(a, ya, b, yb, 1.0)
    assert np.allclose(x, a) and np.allclose(y, ya)
    x, y = mixup(a, ya, b, yb, 0.0)
    assert np.allclose(x, b) and np.allclose(y, yb)


def test_3_labels_still_sum_to_one():
    _, y = mixup(np.zeros(2), np.array([0.0, 1.0, 0.0]), np.ones(2), np.array([1.0, 0.0, 0.0]), 0.3)
    assert np.isclose(y.sum(), 1.0)


def test_4_mixed_pixels_stay_between_the_parents():
    a, b = np.random.RandomState(2).rand(4, 4), np.random.RandomState(3).rand(4, 4)
    x, _ = mixup(a, np.array([1.0]), b, np.array([0.0]), 0.6)
    assert (x <= np.maximum(a, b) + 1e-12).all() and (x >= np.minimum(a, b) - 1e-12).all()


def test_5_sample_lambda_uses_one_beta_draw():
    assert np.isclose(sample_lambda(0.4, np.random.RandomState(7)), np.random.RandomState(7).beta(0.4, 0.4))


def test_6_alpha_controls_how_extreme_lambda_is():
    rng = np.random.RandomState(0)
    small = np.array([sample_lambda(0.1, rng) for _ in range(2000)])
    big = np.array([sample_lambda(5.0, rng) for _ in range(2000)])
    assert np.mean((small < 0.1) | (small > 0.9)) > 0.5 > np.mean((big < 0.1) | (big > 0.9))


def test_7_inputs_untouched():
    a, ya = np.random.RandomState(4).rand(3), np.array([1.0, 0.0])
    sa, sy = a.copy(), ya.copy()
    mixup(a, ya, a + 1, 1 - ya, 0.5)
    assert np.array_equal(a, sa) and np.array_equal(ya, sy)
