"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
ddim_step = _module.ddim_step
AB = np.cumprod(1 - np.linspace(0.05, 0.3, 8))


def test_1_final_step_returns_the_clean_estimate():
    x0 = np.array([1.0, -2.0])
    eps = np.array([0.3, 0.7])
    xt = np.sqrt(AB[5]) * x0 + np.sqrt(1 - AB[5]) * eps
    assert np.allclose(ddim_step(xt, eps, 5, -1, AB), x0)


def test_2_true_noise_jumps_exactly_to_the_forward_sample_at_t_prev():
    rng = np.random.RandomState(0)
    x0, eps = rng.randn(6), rng.randn(6)
    xt = np.sqrt(AB[6]) * x0 + np.sqrt(1 - AB[6]) * eps
    for t_prev in (5, 3, 0):
        expected = np.sqrt(AB[t_prev]) * x0 + np.sqrt(1 - AB[t_prev]) * eps
        assert np.allclose(ddim_step(xt, eps, 6, t_prev, AB), expected)


def test_3_hand_computed():
    out = ddim_step(np.array([2.0]), np.array([1.0]), 3, 1, AB)
    x0 = (2.0 - np.sqrt(1 - AB[3])) / np.sqrt(AB[3])
    assert np.allclose(out, [np.sqrt(AB[1]) * x0 + np.sqrt(1 - AB[1])])


def test_4_deterministic():
    x, e = np.random.RandomState(1).randn(3), np.random.RandomState(2).randn(3)
    assert np.array_equal(ddim_step(x, e, 4, 2, AB), ddim_step(x, e, 4, 2, AB))


def test_5_same_level_is_the_identity():
    x, e = np.random.RandomState(3).randn(4), np.random.RandomState(4).randn(4)
    assert np.allclose(ddim_step(x, e, 4, 4, AB), x)


def test_6_chain_of_steps_with_true_noise_stays_on_the_path():
    rng = np.random.RandomState(5)
    x0, eps = rng.randn(5), rng.randn(5)
    x = np.sqrt(AB[7]) * x0 + np.sqrt(1 - AB[7]) * eps
    for t, tp in [(7, 4), (4, 2), (2, -1)]:
        x = ddim_step(x, eps, t, tp, AB)
    assert np.allclose(x, x0)


def test_7_inputs_untouched():
    x, e = np.random.RandomState(6).randn(3), np.random.RandomState(7).randn(3)
    s1, s2 = x.copy(), e.copy()
    ddim_step(x, e, 5, 1, AB)
    assert np.array_equal(x, s1) and np.array_equal(e, s2)
