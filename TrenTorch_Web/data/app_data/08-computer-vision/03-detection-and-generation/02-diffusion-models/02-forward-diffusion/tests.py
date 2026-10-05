"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
q_sample = _module.q_sample
snr = _module.snr
AB = np.array([0.81, 0.25, 0.01])


def test_1_hand_computed():
    out = q_sample(np.array([10.0]), 0, AB, np.array([-10.0]))
    assert np.allclose(out, [0.9 * 10 + np.sqrt(0.19) * -10])


def test_2_alpha_bar_near_one_returns_the_signal():
    assert np.allclose(q_sample(np.array([3.0]), 0, np.array([1.0 - 1e-12]), np.array([5.0])), 3.0, atol=1e-5)


def test_3_alpha_bar_near_zero_returns_the_noise():
    assert np.allclose(q_sample(np.array([3.0]), 0, np.array([1e-12]), np.array([5.0])), 5.0, atol=1e-5)


def test_4_unit_variance_is_preserved():
    rng = np.random.RandomState(0)
    x0, eps = rng.randn(200000), rng.randn(200000)
    for t in range(3):
        assert abs(q_sample(x0, t, AB, eps).var() - 1.0) < 0.02


def test_5_same_noise_gives_deterministic_output_and_shapes():
    x0, eps = np.ones((2, 3)), np.full((2, 3), 0.5)
    a, b = q_sample(x0, 1, AB, eps), q_sample(x0, 1, AB, eps)
    assert a.shape == (2, 3) and np.array_equal(a, b)


def test_6_snr_hand_computed_and_decreasing():
    s = snr(AB)
    assert np.allclose(s, [0.81 / 0.19, 0.25 / 0.75, 0.01 / 0.99]) and (np.diff(s) < 0).all()


def test_7_inputs_untouched():
    x0, eps = np.random.RandomState(1).randn(4), np.random.RandomState(2).randn(4)
    s1, s2 = x0.copy(), eps.copy()
    q_sample(x0, 2, AB, eps)
    assert np.array_equal(x0, s1) and np.array_equal(eps, s2)
